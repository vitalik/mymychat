import asyncio
import traceback
from django.core.management.color import make_style
from pydantic_ai import Agent
from chat.models import Prompt
from chat.redis_pubsub import pubsub
from llms.dummy import create_dummy_model


class LLMWorker:
    def __init__(self):
        self.running = True
        self.style = make_style()

    async def run(self):
        self.log('Starting LLM worker...', 'SUCCESS')
        while self.running:
            try:
                await self.process_queued_prompts()
                await asyncio.sleep(0.2)
            except Exception as e:
                self.log(f'Error in worker loop: {e}', 'ERROR')
                self.log(traceback.format_exc(), 'ERROR')
                await asyncio.sleep(3)  # Wait longer on error

    async def process_queued_prompts(self):
        prompts = []
        async for prompt in Prompt.objects.filter(status='queued'):
            prompts.append(prompt)

        # Process each prompt
        for prompt in prompts:
            asyncio.create_task(self.process_prompt(prompt))

    async def process_prompt(self, prompt):
        try:
            # Access prompt data directly (since we're in async context)
            prompt_id = prompt.id
            # Use select_related to fetch the chat in one query
            prompt = await Prompt.objects.select_related('chat').aget(id=prompt_id)
            chat_uid = prompt.chat.uid
            chat_model = prompt.chat.model

            # Mark as running
            prompt.status = 'running'
            await prompt.asave()

            # Publish status update
            await pubsub.publish_status(chat_uid, prompt_id, 'running')

            self.log(f'Processing prompt {prompt_id} for chat {chat_uid} using model {chat_model}')

            # Create appropriate model based on chat.model
            if chat_model == 'dummy':
                model = create_dummy_model()
                agent = Agent(model=model)
            else:
                agent = Agent(model=chat_model)

            # Process with pydantic-ai streaming
            async with agent.run_stream(prompt.input_text) as result:
                async for message in result.stream_text(delta=True):
                    # Append each chunk to output_text
                    if prompt.output_text:
                        prompt.output_text += message
                    else:
                        prompt.output_text = message
                    await prompt.asave()

                    # Publish chunk to Redis
                    await pubsub.publish_chunk(chat_uid, prompt_id, message)

            # Mark as finished
            prompt.status = 'finished'
            prompt.result = 'success'
            await prompt.asave()

            # Publish completion status
            await pubsub.publish_status(chat_uid, prompt_id, 'finished')

            self.log(f'Completed prompt {prompt_id}', 'SUCCESS')

        except Exception as e:
            self.log(f'Error processing prompt: {e}', 'ERROR')
            self.log(traceback.format_exc(), 'ERROR')

            # Mark as failed
            prompt.status = 'finished'
            prompt.result = 'failure'
            await prompt.asave()

    def stop(self):
        self.running = False

    def log(self, message, style=None):
        if style == 'SUCCESS':
            print(self.style.SUCCESS(message))
        elif style == 'ERROR':
            print(self.style.ERROR(message))
        elif style == 'WARNING':
            print(self.style.WARNING(message))
        else:
            print(message)

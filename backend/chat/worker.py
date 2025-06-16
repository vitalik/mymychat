import os
import json
import asyncio
import traceback
from django.core.management.color import make_style
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_ai.providers.openrouter import OpenRouterProvider
from chat.models import Prompt
from chat.redis_pubsub import pubsub
from llms.dummy import create_dummy_model
from userprofile.utils import get_userprofile


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

    async def process_prompt(self, prompt: Prompt):
        try:
            # Access prompt data directly (since we're in async context)
            prompt_id = prompt.id
            # Use select_related to fetch the chat and user in one query (async hook)
            prompt = await Prompt.objects.select_related('chat__user').aget(id=prompt_id)
            chat_uid = prompt.chat.uid
            chat_model = prompt.chat.model
            chat_user = prompt.chat.user

            # Mark as running
            prompt.status = 'running'
            await prompt.asave()

            # Publish status update
            await pubsub.publish_status(chat_uid, prompt_id, 'running')

            self.log(f'Processing prompt {prompt_id} for chat {chat_uid} using model {chat_model}')

            # Get user profile for API keys
            user_profile = await get_userprofile(chat_user)

            # Parse provider and model
            provider, model_name = chat_model.split(':', 1)

            # Get system prompt from chat if available
            system_prompt = ()  # empty
            if prompt.chat.system_prompt:
                system_prompt = prompt.chat.system_prompt.text

            # 1) Create appropriate agent based on provider --------------------------------------------------------
            if provider == 'dummy':
                agent_model = create_dummy_model()
                agent = Agent(model=agent_model, system_prompt=system_prompt)

            elif provider == 'openai':
                key = get_openai_key(user_profile)
                agent = Agent(model=model_name, api_key=key, system_prompt=system_prompt)

            elif provider == 'openrouter':
                key = get_openrouter_key(user_profile)
                agent_model = OpenAIModel(
                    model_name,
                    provider=OpenRouterProvider(api_key=user_profile.openrouter_key),
                )
                agent = Agent(model=agent_model, system_prompt=system_prompt)
            else:
                raise ValueError(f"Unknown provider: {provider}")

            # 2) Load previous prompt messages context ----------------------------------------------------------
            history = None
            prev_prompt = (
                await Prompt.objects.filter(chat_id=prompt.chat_id).exclude(id=prompt.id).order_by('-created').afirst()
            )
            if prev_prompt:
                history = ModelMessagesTypeAdapter.validate_python(prev_prompt.llm_messages)

            # print(history)

            # 3) Process with pydantic-ai streaming -------------------------------------------------------------
            async with agent.run_stream(prompt.input_text, message_history=history) as result:
                async for chunk in result.stream_text(delta=True):
                    # Append each chunk to output_text
                    prompt.output_text += chunk
                    await prompt.asave()
                    await pubsub.publish_chunk(chat_uid, prompt_id, chunk)

                prompt.llm_messages = json.loads(result.all_messages_json().decode('utf-8'))

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
            prompt.output_text += traceback.format_exc()
            # TODO: ^ this not really nice - but let's keep it simple for now
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


def get_openrouter_key(profile) -> str:
    if profile.openrouter_key:
        return profile.openrouter_key
    try:
        return os.environ['OPENROUTER_API_KEY']
    except KeyError:
        raise ValueError("OpenRouter API key not configured in user profile or environment variables") from None


def get_openai_key(profile) -> str:
    if profile.openai_key:
        return profile.openai_key
    try:
        return os.environ['OPENAI_API_KEY']
    except KeyError:
        raise ValueError("OpenAI API key not configured in user profile or environment variables") from None

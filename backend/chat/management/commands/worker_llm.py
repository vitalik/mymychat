import os
import asyncio
from django.core.management.base import BaseCommand
from chat.worker import LLMWorker


class Command(BaseCommand):
    help = 'Worker for processing LLM prompts'

    def handle(self, *args, **options):
        if 'OPENAI_API_KEY' not in os.environ:
            self.stderr.write(self.style.ERROR('WARN: OPENAI_API_KEY environment variable is not set.'))

        worker = LLMWorker()
        try:
            asyncio.run(worker.run())
        except KeyboardInterrupt:
            print('\nShutting down worker...')
            worker.stop()

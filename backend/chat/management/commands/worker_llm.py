import asyncio
from django.core.management.base import BaseCommand
from chat.worker import LLMWorker


class Command(BaseCommand):
    help = 'Worker for processing LLM prompts'

    def handle(self, *args, **options):
        worker = LLMWorker()
        try:
            asyncio.run(worker.run())
        except KeyboardInterrupt:
            print('\nShutting down worker...')
            worker.stop()

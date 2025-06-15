import signal
import os
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        # Simple signal handler that exits immediately
        def signal_handler(signum, frame):
            print(f"\nReceived signal {signum}, exiting immediately...")
            os._exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

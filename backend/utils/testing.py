import time
from django.utils.deprecation import MiddlewareMixin


class SlowMiddleware(MiddlewareMixin):
    """Middleware that adds artificial delay to simulate slow network connections."""

    def process_request(self, request):
        time.sleep(1)
        return None

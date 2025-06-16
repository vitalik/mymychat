import os
from pathlib import Path
from mimetypes import guess_type
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'static'
INDEX_HTML_PATH = STATIC_ROOT / 'index.html'

django_app = get_asgi_application()


class StaticAndSPAFallback:
    def __init__(self, app, static_dir: Path, index_path: Path):
        self.app = app
        self.static_dir = static_dir
        self.index_path = index_path

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        type_ = scope.get("type")

        if type_ != "http":
            return await self.app(scope, receive, send)

        # Bypass for API or admin
        if path.startswith("/api") or path.startswith("/admin"):
            return await self.app(scope, receive, send)

        # Try serving static file if it exists
        static_file = self.static_dir / path.lstrip("/")
        if static_file.exists() and static_file.is_file():
            mime, _ = guess_type(str(static_file))
            headers = [
                (b"content-type", mime.encode() if mime else b"application/octet-stream"),
                (b"content-length", str(static_file.stat().st_size).encode()),
            ]
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": headers,
                }
            )
            with open(static_file, "rb") as f:
                await send(
                    {
                        "type": "http.response.body",
                        "body": f.read(),
                        "more_body": False,
                    }
                )
            return

        # Fallback to index.html for SPA
        if self.index_path.exists():
            stat = self.index_path.stat()
            headers = [
                (b"content-type", b"text/html"),
                (b"content-length", str(stat.st_size).encode()),
            ]
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": headers,
                }
            )
            with open(self.index_path, "rb") as f:
                await send(
                    {
                        "type": "http.response.body",
                        "body": f.read(),
                        "more_body": False,
                    }
                )
        else:
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [(b"content-type", b"text/plain")],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": b"index.html not found",
                }
            )


application = StaticAndSPAFallback(django_app, STATIC_ROOT, INDEX_HTML_PATH)

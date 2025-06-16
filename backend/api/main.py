from ninja import NinjaAPI
from chat.api import router as chat_router
from auth.auth import jwt_bearer_auth
from auth.api import router as auth_router


api = NinjaAPI(auth=jwt_bearer_auth)


api.add_router("/chats", chat_router, tags=["chats"])
api.add_router("/auth", auth_router, tags=["auth"])


@api.get("/settings")
def get_settings(request):
    """Get application settings."""
    return {"language": "en"}


@api.get("/models")
def get_models(request):
    """Get list of available LLM models."""
    return {
        "models": [
            {"id": "dummy", "name": "Dummy Model", "description": "Test model with random text"},
            {"id": "gpt-4o", "name": "GPT-4o", "description": "OpenAI GPT-4o"},
        ]
    }

from ninja import NinjaAPI
from chat.api import router as chat_router
from auth.auth import jwt_bearer_auth
from auth.api import router as auth_router
from userprofile.api import router as profile_router
from llms.providers import get_providers_and_models
from llms.tools import available_tools


api = NinjaAPI(auth=jwt_bearer_auth)


api.add_router("/chats", chat_router, tags=["chats"])
api.add_router("/auth", auth_router, tags=["auth"])
api.add_router("/", profile_router, tags=["profile"])


@api.get("/settings")
def get_settings(request):
    """Get application settings."""
    return {"language": "en"}


@api.get("/models")
def get_models(request):
    """Get list of available LLM models grouped by provider."""
    return get_providers_and_models()


@api.get("/tools")
def get_tools(request):
    """Get list of available tools."""
    return {key: {"name": tool["name"]} for key, tool in available_tools.items()}

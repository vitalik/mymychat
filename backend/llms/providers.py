import httpx
from typing import Optional
from utils.cache import cache


def get_providers_and_models():
    """Get list of available LLM models grouped by provider."""
    providers = [
        {
            "provider": "dummy",
            "models": [{"name": "Dummy Model", "id": "dummy:dummy", "description": "Test model with random text"}],
        },
        {
            "provider": "openai",
            "models": [
                {"name": "GPT-4o", "id": "openai:gpt-4o", "description": "OpenAI GPT-4o"},
                {"name": "GPT-4o Mini", "id": "openai:gpt-4o-mini", "description": "OpenAI GPT-4o Mini"},
            ],
        },
    ]

    # Fetch OpenRouter models with caching
    openrouter_models = get_openrouter_models()
    providers.append({"provider": "openrouter", "models": openrouter_models})

    return providers


@cache(ttl=30 * 60)  # 30 minutes
def get_openrouter_models() -> list:
    response = httpx.get("https://openrouter.ai/api/v1/models", timeout=5.0)
    if response.status_code != 200:
        print(f"Error fetching OpenRouter models: {response.status_code} {response.text}")
        return []
    openrouter_data = response.json()
    result = []

    # Get all models
    for model in openrouter_data.get("data", []):
        result.append(
            {
                "name": model.get("name", model["id"]),
                "id": f"openrouter:{model['id']}",
                "description": model.get("description", "")[:100],
            }
        )

    return result

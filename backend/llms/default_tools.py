from django.utils import timezone
from pydantic_ai import RunContext
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool as create_duckduckgo_search_tool


def current_time(ctx: RunContext) -> str:
    """Returns the current time in ISO format."""
    return timezone.now().isoformat()


duckduckgo_search = create_duckduckgo_search_tool()


TOOLS = {
    'current_time': {
        'name': 'Get current time',
        'callback': current_time,
    },
    'duckduckgo_search': {
        'name': 'DuckDuckGo Search',
        'callback': duckduckgo_search,
    },
}

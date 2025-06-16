from .default_tools import TOOLS as DEFAULT_TOOLS


def get_available_tools():
    result = {}
    result.update(DEFAULT_TOOLS)
    return result


available_tools = get_available_tools()

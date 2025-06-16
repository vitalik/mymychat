import time
import functools
from typing import Any, Callable, Optional


class CacheEntry:
    def __init__(self, value: Any, timestamp: float):
        self.value = value
        self.timestamp = timestamp


# Global cache storage
_cache_storage: dict[str, CacheEntry] = {}


def cache(ttl: int):
    """
    Cache decorator with TTL (time-to-live) support.

    Args:
        ttl: Time to live in seconds

    Usage:
        @cache(ttl=30*60)  # 30 minutes
        def expensive_function():
            return some_expensive_operation()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from function name and arguments
            cache_key = f"{func.__module__}.{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            current_time = time.time()

            # Check if we have valid cached data
            if cache_key in _cache_storage:
                entry = _cache_storage[cache_key]
                if current_time - entry.timestamp < ttl:
                    return entry.value

            # Call the function and cache the result
            try:
                result = func(*args, **kwargs)
                _cache_storage[cache_key] = CacheEntry(result, current_time)
                return result
            except Exception as e:
                # If function fails and we have expired cache, return it as fallback
                if cache_key in _cache_storage:
                    return _cache_storage[cache_key].value
                raise e

        return wrapper

    return decorator


def clear_cache(func: Optional[Callable] = None) -> None:
    """
    Clear cache for a specific function or all cache if no function provided.

    Args:
        func: Function to clear cache for, or None to clear all cache
    """
    if func is None:
        _cache_storage.clear()
    else:
        # Remove all cache entries for this function
        prefix = f"{func.__module__}.{func.__name__}:"
        keys_to_remove = [key for key in _cache_storage.keys() if key.startswith(prefix)]
        for key in keys_to_remove:
            del _cache_storage[key]

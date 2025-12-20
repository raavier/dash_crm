"""
In-memory cache layer for Dashboard CRM API.
Uses cachetools for TTL-based caching with automatic expiration.
"""
from cachetools import TTLCache
from functools import wraps
from typing import Any, Callable, Optional
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class DashboardCache:
    """
    Thread-safe in-memory cache with TTL support.

    Uses cachetools.TTLCache which automatically expires entries after TTL.
    Suitable for single-server deployments.

    For multi-server deployments, consider Redis instead.
    """

    def __init__(self, maxsize: int = 1000, ttl: int = 14400):
        """
        Initialize cache.

        Args:
            maxsize: Maximum number of items in cache (default: 1000)
            ttl: Time-to-live in seconds (default: 14400 = 4 hours)
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.ttl = ttl
        logger.info(f"Cache initialized with maxsize={maxsize}, ttl={ttl}s ({ttl/3600}h)")

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """
        Generate unique cache key based on function name and arguments.

        Args:
            func_name: Name of the function
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Hash string to use as cache key
        """
        # Convert args to hashable format
        key_parts = [func_name]

        # Add args
        for arg in args:
            if hasattr(arg, '__dict__'):
                # For objects (like DashboardFilters), convert to dict
                key_parts.append(json.dumps(arg.__dict__, sort_keys=True, default=str))
            else:
                key_parts.append(str(arg))

        # Add kwargs
        if kwargs:
            key_parts.append(json.dumps(kwargs, sort_keys=True, default=str))

        # Generate hash
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.cache.get(key)
            if value is not None:
                logger.debug(f"Cache HIT: {key}")
            else:
                logger.debug(f"Cache MISS: {key}")
            return value
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        try:
            self.cache[key] = value
            logger.debug(f"Cache SET: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")

    def delete(self, key: str) -> None:
        """Delete specific key from cache."""
        try:
            if key in self.cache:
                del self.cache[key]
                logger.info(f"Cache DELETE: {key}")
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")

    def clear(self) -> None:
        """Clear entire cache."""
        try:
            self.cache.clear()
            logger.info("Cache CLEARED")
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")

    def stats(self) -> dict:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "ttl": self.ttl,
            "ttl_hours": round(self.ttl / 3600, 2)
        }


# Global cache instance
cache = DashboardCache(maxsize=1000, ttl=14400)  # 4 hours TTL


def cached(func: Callable) -> Callable:
    """
    Decorator to cache function results.

    Usage:
        @cached
        def get_metrics(filters: DashboardFilters) -> MetricsData:
            # expensive query
            return result

    The decorator will:
    1. Generate a unique key based on function name and arguments
    2. Check if result is in cache
    3. Return cached result if available
    4. Execute function and cache result if not available
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Skip 'self' argument for methods
        cache_args = args[1:] if args and hasattr(args[0], '__class__') else args

        # Generate cache key
        cache_key = cache._generate_key(func.__name__, cache_args, kwargs)

        # Try to get from cache
        result = cache.get(cache_key)

        if result is not None:
            logger.info(f"Cache HIT for {func.__name__}")
            return result

        # Cache miss - execute function
        logger.info(f"Cache MISS for {func.__name__} - executing query")
        result = func(*args, **kwargs)

        # Store in cache
        cache.set(cache_key, result)

        return result

    return wrapper


def invalidate_cache_pattern(pattern: str) -> int:
    """
    Invalidate all cache keys matching a pattern.

    Args:
        pattern: String to match in cache keys (e.g., "get_metrics")

    Returns:
        Number of keys deleted
    """
    deleted = 0
    keys_to_delete = []

    # Find matching keys
    for key in list(cache.cache.keys()):
        if pattern in key:
            keys_to_delete.append(key)

    # Delete keys
    for key in keys_to_delete:
        cache.delete(key)
        deleted += 1

    logger.info(f"Invalidated {deleted} cache keys matching pattern: {pattern}")
    return deleted


# Convenience functions
def clear_all_cache() -> None:
    """Clear entire cache."""
    cache.clear()


def get_cache_stats() -> dict:
    """Get cache statistics."""
    return cache.stats()

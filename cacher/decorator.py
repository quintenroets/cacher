from functools import wraps

from . import cacheslot


def cache(key_reducer=None):
    """
    A decorator to cache function results.
    Decorated functions are only executed if result is not present in cache.
    The arguments of the function can be any nested complex object

    Use as:

    from cacher import cache

    @cache
    def long_function(complex_object):
        ..

    """

    def cache_decorator(function):
        @wraps(function)
        def wrapped_function(*args, **kwargs):
            cache_slot = cacheslot.CacheSlot(key_reducer, function, args, kwargs)
            value = cache_slot.value
            if value is cacheslot.CACHE_MISS:
                value = function(*args, **kwargs)
                cache_slot.value = value
            return value

        return wrapped_function

    return cache_decorator

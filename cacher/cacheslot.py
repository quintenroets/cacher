import pickle

from . import hashing
from .path import Path

CACHE_MISS = "CACHE_MISS"


class CacheSlot:
    def __init__(self, function, args, kwargs, key_reducer=None, cache_path=None):
        # change cache key when implementation changes
        cache_keys = (function, args, kwargs)
        if cache_path is None:
            cache_path = Path.cache

        self.location = (
            cache_path
            / function.__module__.replace(".", "_")
            / function.__name__
            / hashing.compute_hash(key_reducer, cache_keys)
        )

    @property
    def value(self):
        try:
            value = self.load_value()
        except (pickle.UnpicklingError, EOFError):
            # discard values of corrupted or empty slots
            # Don't use None because some functions effectively have None as cached result
            value = CACHE_MISS
        return value

    def load_value(self):
        with self.location.open("rb") as fp:
            return pickle.Unpickler(fp).load()

    @value.setter
    def value(self, value):
        self.location.byte_content = pickle.dumps(value)

import inspect
import pickle

from plib import Path

from . import hashing

CACHE_MISS = "CACHE_MISS"


class CacheSlot:
    def __init__(self, key_reducer, function, args, kwargs):
        # change cache key when implementation changes
        function_implementation = inspect.getsource(function)
        cache_keys = (function_implementation, args, kwargs)
        self.location = (
            Path.assets
            / "cache"
            / function.__module__.replace(".", "_")
            / function.__name__
            / hashing.compute_hash(key_reducer, cache_keys)
        )

    def get_value(self):
        if self.location.exists():
            with self.location.open("rb") as fp:
                try:
                    value = pickle.Unpickler(fp).load()
                except pickle.UnpicklingError:
                    # recalculate corrupted files
                    value = CACHE_MISS
        else:
            # Don't use None because some functions effectively have None as cached result
            value = CACHE_MISS
        return value

    def set_value(self, value):
        with self.location.open("wb") as fp:
            pickle.dump(value, fp)

from __future__ import annotations

import hashlib
import inspect
import io
import pickle
from typing import TYPE_CHECKING, Any, Type, get_args, get_type_hints

if TYPE_CHECKING:
    from .caches.base import Reducer


class HashPickler(pickle.Pickler):
    def __init__(self, reducer: Type[Reducer], fp):
        super().__init__(fp)
        if reducer is None:
            from .caches.base import Reducer  # noqa: autoimport

            reducer = Reducer

        self.reducer = reducer
        self.reducers = {}
        for name, method in inspect.getmembers(reducer, predicate=inspect.ismethod):
            type_hints = get_type_hints(method).values()
            argument_type = next(iter(type_hints))
            argument_types = get_args(argument_type) or (argument_type,)
            for argument_type in argument_types:
                self.reducers[argument_type] = method

    def reducer_override(self, obj: Any) -> Any:
        """
        The goal of this pickler is to create hashes of complex objects, not to reconstruct complex objects.
        So mapping does not need to be reversible.
        """
        reducer = self.get_reducer(obj)
        if reducer is None:
            reduction = NotImplemented
        else:
            mapping = reducer(obj)
            str_mapping = str(object_to_bytes(self.reducer, mapping))
            reduction = str, (str_mapping,)

        return reduction

    def get_reducer(self, obj):
        if obj is not str:
            for obj_type, reducer in self.reducers.items():
                if isinstance(obj, obj_type):
                    return reducer


def compute_hash(key_reducer, *args):
    data = object_to_bytes(key_reducer, args)
    # use fast hash function because it is not used for security
    return hashlib.new("sha1", data=data, usedforsecurity=False).hexdigest()


def object_to_bytes(key_reducer: Reducer, args: Any) -> bytes:
    with io.BytesIO() as fp:
        # Use custom pickler to generate bytes from complex structures
        HashPickler(key_reducer, fp).dump(args)
        fp.seek(0)
        return fp.read()

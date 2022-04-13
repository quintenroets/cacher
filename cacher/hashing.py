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
            reducer = Reducer

        self.reductions = {}
        for name, method in inspect.getmembers(reducer, predicate=inspect.ismethod):
            type_hints = get_type_hints(method).values()
            argument_type = next(iter(type_hints))
            argument_types = get_args(argument_type) or (argument_type,)
            for argument_type in argument_types:
                self.reductions[argument_type] = method

    def reducer_override(self, obj: Any) -> Any:
        """
        The goal of this pickler is to create hashes of complex objects, not to reconstruct complex objects.
        So reducer does not need to be a reversible mapping.
        """
        reduction = NotImplemented
        for obj_type, mapping in self.reductions.items():
            if isinstance(obj, obj_type):
                reduction = mapping(obj)
                str_value = (str(pickle.dumps(reduction)),)
                reduction = str, str_value
        return reduction


def compute_hash(key_reducer, *args):
    try:
        hash_function = hashlib.sha256(usedforsecurity=False)
    except TypeError:
        hash_function = hashlib.sha256()

    with io.BytesIO() as fp:
        # use pickler to generate bytes and hash from complex structures
        pickler = HashPickler(key_reducer, fp)
        pickler.dump(args)

        fp.seek(0)
        hash_function.update(fp.read())

    return hash_function.hexdigest()

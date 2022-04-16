import inspect
import io
from types import LambdaType, ModuleType
from typing import Callable, Union

from .. import decorator


class Reducer:
    @classmethod
    def reduce_function(cls, function: Union[Callable, LambdaType]) -> str:
        # assume cache value can change when function implementation changes
        # lambda function: https://www.pythonpool.com/cant-pickle-local-object/
        return inspect.getsource(function)

    @classmethod
    def reduce_module(cls, module: ModuleType) -> str:
        # https://stackoverflow.com/questions/2790828/python-cant-pickle-module-objects-error
        try:
            reduction = inspect.getsource(module)
        except TypeError:
            # cannot access source code of builtin modules but no problem because we assume this code does not change
            reduction = module.__name__
        return reduction

    @classmethod
    def reduce_file_objects(cls, _: Union[io.BytesIO, io.BufferedWriter]) -> str:
        # Closed file pointers cannot and do not need to be pickled for cache functionality
        return ""


cache = decorator.cache(Reducer)

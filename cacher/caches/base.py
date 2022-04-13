import inspect
import io
from types import LambdaType, ModuleType
from typing import Union

from .. import decorator


class Reducer:
    @classmethod
    def reduce_file_objects(cls, _: Union[io.BytesIO, io.BufferedWriter]) -> str:
        # Closed file pointers cannot and do not need to be pickled for cache functionality
        return ""

    @classmethod
    def reduce_lambda_function(cls, function: LambdaType) -> str:
        # https://www.pythonpool.com/cant-pickle-local-object/
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


cache = decorator.cache(Reducer)

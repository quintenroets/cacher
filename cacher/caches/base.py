import inspect
import io
from types import LambdaType, ModuleType
from typing import Callable, Union

from .. import decorator


class Reducer:
    @classmethod
    def reduce_code(cls, code_object: Union[Callable, LambdaType, ModuleType]) -> str:
        # assume cache value can change when function/module implementation changes
        # custom lambda reduction needed:
        #   https://www.pythonpool.com/cant-pickle-local-object/
        # custom module reduction needed:
        #   https://stackoverflow.com/questions/2790828/python-cant-pickle-module-objects-error
        if code_object == str:
            # don't apply custom reduction on str (also a callable) to avoid infinite recursive calls
            # because everything is reduced to a str
            reduction = NotImplemented
            pprint("joe")
        pprint("ja")
        pprint(code_object)
        try:
            reduction = inspect.getsource(code_object)
        except:
            # cannot access source code of builtin function/module
            # but no problem because we assume this code does not change
            reduction = code_object.__name__
        return reduction

    @classmethod
    def reduce_file_objects(cls, _: Union[io.BytesIO, io.BufferedWriter]) -> str:
        # Closed file pointers cannot and do not need to be pickled for cache functionality
        return ""


cache = decorator.cache(Reducer)

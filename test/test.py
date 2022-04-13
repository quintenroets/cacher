import io
import math

from cacher import cache


@cache
def calculate(*args, **kwargs):
    print("calculation started")
    print(args, kwargs)


with io.BytesIO() as fp:
    calculate(fp, lambda x: x, math, {})

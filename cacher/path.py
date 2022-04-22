import plib


class Path(plib.Path):
    @classmethod
    @property
    def cache(cls):
        return plib.Path.assets / "cache"

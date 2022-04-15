# Cache

## Installation

```shell
pip install git+https://github.com/quintenroets/cacher
```

## Usage
Use

```shell
from cacher import cache

@cache
def long_function(..):
    ..

to cache the result of a function
```


Advantages compared to existing projects:
* Each cache result is saved to separate local file. Only results that are effectively needed are loaded.
* The cache entry does not only depend on the arguments and the name of the function, but on the implementation of the function as well. 
* Works on arguments with any complex data type that does not necessarily need to be hashable (e.g dictionary).
* Configurability: custom reductions can be defined based on the object type. This reduction is applied to all objects with the corresponding type, even when they belong to complex, composed larger objects. For example, for larger datasets, the user can decide to only hash the length of the dataset and a few samples, instead of the whole dataset. This can lead to huge speedups. The risk on collisions depends on the use case. (see caches directory)
* 3 cachers available out-of-the-box: (can be extended with custom reducers, see above):
  * from cacher import cache
  * from cacher.caches.deep_learning import cache
  * from cacher.caches.speedup_deep_learning import cache`

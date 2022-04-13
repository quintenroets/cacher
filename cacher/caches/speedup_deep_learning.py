from typing import Tuple

import numpy as np
import torch
from torch.utils.data import Dataset

from .. import decorator
from . import deep_learning


class Reducer(deep_learning.Reducer):
    @classmethod
    def reduce_np_array(cls, array: np.ndarray) -> Tuple[Tuple[int], np.ndarray]:
        length = len(array)
        # only use part of array for speedup
        data = array[13 ** 17 % length] if length > 0 else array
        return array.shape, data

    @classmethod
    def reduce_model(cls, model: torch.nn.Module):
        state = super(Reducer, cls).reduce_model(model)
        length = len(state)
        values = list(state.values())
        # only use part of state for speedup
        values = values[0], values[length // 2], values[-1]
        values = tuple(cls.reduce_tensor(v) for v in values)
        return values

    @classmethod
    def reduce_dataset(cls, dataset: Dataset):
        # ignore len(dataset) warning
        length = len(dataset)  # noqa
        # only use part of dataset for speedup
        data = dataset[13 ** 17 % length] if length > 0 else torch.Tensor([])
        if isinstance(data, tuple):
            data, label = data
        else:
            label = None
        return length, cls.reduce_tensor(data), label

    @classmethod
    def reduce_tensor(cls, tensor: torch.Tensor):
        np_array = tensor.detach().cpu().numpy()
        return cls.reduce_np_array(np_array)


cache = decorator.cache(Reducer)

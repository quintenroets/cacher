from typing import Any, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset

from .. import decorator
from . import deep_learning


class Reducer(deep_learning.Reducer):
    @classmethod
    def reduce_np_array(cls, array: np.ndarray) -> Tuple[Tuple[int], Any]:
        shape = array.shape
        # only use part of array for speedup
        data = array[13 ** 17 % shape[-1]] if shape else []
        return shape, data

    @classmethod
    def reduce_model(cls, model: torch.nn.Module):
        state = super(Reducer, cls).reduce_model(model)
        length = len(state)
        values = list(state.values())
        if length > 0:
            # only use part of state for speedup
            reduction_indices = (0, length // 2, -1)
            reduction = tuple(values[i] for i in reduction_indices)
        else:
            reduction = []
        return reduction

    @classmethod
    def reduce_dataset(cls, dataset: Dataset):
        # ignore len(dataset) warning
        length = len(dataset)  # noqa
        # only use part of dataset for speedup
        data = dataset[13 ** 17 % length] if length > 0 else []
        if isinstance(data, tuple):
            data, label = data
        else:
            label = None
        return length, data, label

    @classmethod
    def reduce_tensor(cls, tensor: torch.Tensor):
        return tensor.detach().cpu().numpy()


cache = decorator.cache(Reducer)

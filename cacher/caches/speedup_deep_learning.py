import math
from typing import Any, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset

from .. import decorator
from . import deep_learning

SEED_VALUE = 493


class Reducer(deep_learning.Reducer):
    @classmethod
    def reduce_np_array(cls, array: np.ndarray) -> Tuple[Tuple[int], Any]:
        shape = array.shape
        if shape and math.prod(shape) > 10000:
            # only use part of array large for speedup
            length = shape[0] if shape else 0
            data = (array[13**17 % length]) if length > 0 else []
            reduction = shape, data
        elif shape:
            reduction = list(array)
        else:
            reduction = array.item()
        return reduction

    @classmethod
    def reduce_model(cls, model: torch.nn.Module):
        weights, implementation = super(Reducer, cls).reduce_model(model)

        length = len(weights)
        if length > 0:
            # only use part of weights for speedup
            values = list(weights.values())
            reduction_indices = (0, length // 2, -1)
            weights = tuple(values[i] for i in reduction_indices)

        return weights, implementation

    @classmethod
    def reduce_dataset(cls, dataset: Dataset):
        # ignore len(dataset) warning
        length = len(dataset)  # noqa

        # fix random seed to have deterministic hash for datasets with random augmentation
        torch.random.manual_seed(SEED_VALUE)

        # only use part of dataset for speedup
        data = dataset[13**17 % length] if length > 0 else []
        if isinstance(data, tuple):
            data, label = data
        else:
            label = None

        return length, data, label

    @classmethod
    def reduce_tensor(cls, tensor: torch.Tensor):
        return tensor.detach().cpu().numpy()


cache = decorator.cache(Reducer)

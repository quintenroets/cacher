import torch

from .. import decorator
from . import base


class Reducer(base.Reducer):
    @classmethod
    def reduce_model(cls, model: torch.nn.Module):
        """
        Avoid pickling _forward_hooks of model: implemented as OrderedDict with nondeterministic keys
        Model outputs determined by:
            - model weights
            - class implementation (forward method)
        """
        return model.state_dict(), model.__class__

    @classmethod
    def reduce_tensor(cls, tensor: torch.Tensor):
        # Pickling a Tensor or a Storage is not deterministic #39382 => convert to numpy
        # https://github.com/pytorch/pytorch/issues/3938
        return tensor.detach().cpu().numpy()


cache = decorator.cache(Reducer)

from django_erd_generator.definitions.models import (
    ModelArray as BaseModelArray,
    ModelDefinition,
)
from .models import Customer, Order, Product, Region


class ModelArray(BaseModelArray):
    def get_models(*args, **kwargs) -> BaseModelArray:
        arr = ModelArray(**kwargs)
        for cls in [Customer, Product, Order, Region]:
            arr.append(ModelDefinition(cls, **kwargs))
        return arr

from django_erd_generator.definitions.models import ModelArray, ModelDefinition
from .models import Customer, Order, Product, Region


class ModelArray(ModelArray):
    def get_models(*args, **kwargs) -> ModelArray:
        arr = ModelArray(**kwargs)
        for cls in [Customer, Product, Order, Region]:
            arr.append(ModelDefinition(cls, **kwargs))
        return arr

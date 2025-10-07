from typing import Dict
from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.models import ModelDefinition
from tests.utils import ModelArray


def get_data_dictionary() -> Dict[str, ModelDefinition]:
    model_map = {}
    for model in ModelArray.get_models(dialect=Dialect.MERMAID):
        name = f"{(cls := model.django_model)._meta.app_label}.models.{cls.__name__}"
        model_map[name] = model
    return model_map

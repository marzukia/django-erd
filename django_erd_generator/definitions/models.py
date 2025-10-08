from typing import Union
from django_erd_generator.contrib.dialects import (
    MODEL_PATTERN_LOOKUP,
    OUTPUT_PATTERN_LOOKUP,
    Dialect,
)
from django_erd_generator.definitions.base import BaseArray, BaseDefinition
from django_erd_generator.definitions.fields import FieldArray, FieldDefinition
from django_erd_generator.definitions.relationships import RelationshipArray
from django.db import models
import django.apps as d


class ModelDefinition(BaseDefinition):
    def __init__(self, model: models.Model, dialect: Dialect = Dialect.MERMAID) -> None:
        self.django_model = model
        self.dialect = dialect
        self.fields = self.django_model
        self.relationships = self.django_model
        self.name = model.__name__

    @property
    def fields(self) -> list[FieldDefinition]:
        return self._fields

    @fields.setter
    def fields(self, model: models.Model) -> None:
        valid_fields = FieldArray(dialect=self.dialect)
        for field in model._meta.get_fields():
            if field.concrete:
                definition = FieldDefinition(field, dialect=self.dialect)
                if definition.data_type:
                    valid_fields.append(definition)
        valid_fields.sort(key=lambda x: x.primary_key, reverse=True)
        self._fields = valid_fields

    @property
    def relationships(self) -> RelationshipArray:
        return self._relationships

    @relationships.setter
    def relationships(self, django_model: models.Model) -> None:
        valid_relationships = RelationshipArray(dialect=self.dialect)
        for field in django_model._meta.get_fields():
            relationship = FieldDefinition.get_relationship(field, dialect=self.dialect)
            if relationship and relationship.rel != "one_to_many":
                # NOTE: one_to_many and many_to_one are duplicated, so we only take one
                # of these values.
                valid_relationships.append(relationship)
        self._relationships = valid_relationships

    def to_string(self) -> str:
        return MODEL_PATTERN_LOOKUP[self.dialect].format(
            model_name=self.django_model.__name__,
            model_fields=self.fields.to_string(),
        )


class ModelArray(BaseArray):
    @classmethod
    def get_models(
        cls,
        valid_apps: Union[list[str], None] = None,
        dialect: Dialect = Dialect.MERMAID,
    ) -> "ModelArray":
        _dialect = Dialect(dialect)
        valid = cls(dialect=_dialect)

        models = [i for i in d.apps.get_models()]
        for model in models:
            if not valid_apps or (model._meta.app_label in valid_apps):
                valid.append(ModelDefinition(model, dialect=_dialect))
        return valid

    @property
    def relationships(self) -> RelationshipArray:
        models = [*self]
        valid = []
        unique = RelationshipArray(dialect=self.dialect)
        models.sort(key=lambda x: (len(x.relationships), x.name))
        for model in models:
            for relationship in model.relationships:
                if relationship.to_string() not in valid:
                    if relationship.inverse().to_string() not in valid:
                        valid.append(relationship.to_string())
                        unique.append(relationship)
        return unique

    def to_string(self) -> str:
        models_string = "\n".join([i.to_string() for i in self])
        return OUTPUT_PATTERN_LOOKUP[self.dialect].format(
            models=models_string,
            relationships=self.relationships.to_string(),
        )

from django.db import models

from django_erd_generator.contrib.dialects import (
    REL_CODE_LOOKUP,
    REL_PATTERN_LOOKUP,
    Dialect,
)
from django_erd_generator.definitions.base import BaseArray, BaseDefinition


class Relationship(BaseDefinition):
    def __init__(
        self,
        field: models.Field = None,
        rel_code: str = None,
        dialect: Dialect = Dialect.MERMAID,
        from_model: str = None,
        from_field: str = None,
        to_model: str = None,
        to_field: str = None,
    ):
        self.dialect = dialect
        self.rel = rel_code
        if field:
            self.from_model = field.related_model.__name__
            self.from_field = field.related_model._meta.pk.attname
            self.to_model = field.model.__name__
            self.to_field = field.attname if hasattr(field, "attname") else field.name
            if self.rel in ["many_to_many", "one_to_one"]:
                self.to_field = field.model._meta.pk.attname
                self.from_field = field.related_model._meta.pk.attname
        else:
            self.to_model = to_model
            self.to_field = to_field
            self.from_model = from_model
            self.from_field = from_field

    def inverse(self) -> "Relationship":
        split_rel = self.rel.split("_")
        inverse_rel = "_".join([split_rel[-1], split_rel[1], split_rel[0]])
        return Relationship(
            from_field=self.to_field,
            from_model=self.to_model,
            to_field=self.from_field,
            to_model=self.from_model,
            rel_code=inverse_rel,
            dialect=self.dialect,
        )

    def to_string(self) -> str:
        rel_code = REL_CODE_LOOKUP[self.dialect][self.rel]
        pattern = REL_PATTERN_LOOKUP[self.dialect]
        return pattern.format(
            rel_code=rel_code,
            from_model=self.from_model,
            from_field=self.from_field,
            to_model=self.to_model,
            to_field=self.to_field,
        )


class RelationshipArray(BaseArray):
    pass

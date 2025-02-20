import re
from django.db import models, connection

from django_erd_generator.contrib.dialects import (
    FIELD_PATTERN_LOOKUP,
    PK_PATTERN_LOOKUP,
    Dialect,
)
from django_erd_generator.definitions.base import BaseArray, BaseDefinition
from django_erd_generator.definitions.relationships import Relationship


class FieldDefinition(BaseDefinition):
    def __init__(self, field: models.Field, dialect: Dialect = Dialect.MERMAID) -> None:
        self.django_field = field
        self.dialect = dialect
        self.col_name = self.django_field
        self.data_type = self.django_field
        self.primary_key = self.django_field

    @classmethod
    def get_relationship(
        self,
        field: models.Field,
        dialect: Dialect = Dialect.MERMAID,
    ) -> Relationship:
        rel_codes = ["one_to_many", "one_to_one", "many_to_one", "many_to_many"]
        if hasattr(field, "is_relation"):
            for rel_code in rel_codes:
                if getattr(field, rel_code, None):
                    return Relationship(field, rel_code, dialect=dialect)
        return None

    @classmethod
    def get_data_type(self, field: models.Field, dialect: Dialect) -> str:
        pattern = r"(\w+)\(([^)]+)\)"
        data_type = field.cast_db_type(connection)
        if data_type:
            matches = re.findall(pattern, data_type)
            args = None
            if matches:
                data_type, args = matches[0]
            if dialect is Dialect.MERMAID:
                # NOTE: MermaidJS erDiagram does not currently support spaces in either the field name,
                # or the data type. It incorrectly attempts to parse it as a comment.
                # More information: https://github.com/mermaid-js/mermaid/issues/1546
                data_type = data_type.replace(" ", "_")
            return {
                "data_type": data_type.lower(),
                "args": args,
            }
        return None

    @property
    def col_name(self) -> str:
        return self._col_name

    @col_name.setter
    def col_name(self, field: models.Field) -> None:
        self._col_name = field.attname

    @property
    def data_type(self) -> str:
        return self._data_type

    @data_type.setter
    def data_type(self, field: models.Field) -> None:
        self._data_type = self.get_data_type(field, self.dialect)

    @property
    def primary_key(self) -> bool:
        return self._primary_key

    @primary_key.setter
    def primary_key(self, field: models.Field) -> None:
        self._primary_key = field.primary_key

    def to_string(self) -> str:
        pattern = FIELD_PATTERN_LOOKUP[self.dialect]
        pk = PK_PATTERN_LOOKUP[self.dialect] if self.primary_key else ""
        col_name = self.col_name
        if self.dialect is Dialect.PLANTUML and self.primary_key:
            col_name = "*" + self.col_name
        return pattern.format(
            col_name=col_name,
            data_type=self.data_type["data_type"],
            primary_key=pk,
        )

    def __repr__(self) -> str:
        return self.to_string()


class FieldArray(BaseArray):
    pass

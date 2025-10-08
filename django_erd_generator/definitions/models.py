"""
Django model definitions for ERD generation.

This module provides classes for representing Django models and their collections
in various ERD dialects (Mermaid, PlantUML, dbdiagram). It extracts model metadata,
fields, and relationships to generate structured representations suitable for
different diagramming tools.
"""

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
    """
    Represents a single Django model for ERD generation.

    This class encapsulates a Django model and provides methods to extract
    and format its fields and relationships according to different ERD dialects.
    It automatically processes model metadata to create field definitions and
    relationship mappings suitable for diagram generation.

    Attributes:
        django_model: The Django model class being represented
        dialect: The ERD dialect (Mermaid, PlantUML, dbdiagram) for output formatting
        fields: Array of field definitions for this model
        relationships: Array of relationship definitions for this model
        name: The model class name

    Example:
        >>> from django_erd_generator.contrib.dialects import Dialect
        >>> model_def = ModelDefinition(MyModel, dialect=Dialect.MERMAID)
        >>> print(model_def.to_string())
    """

    def __init__(self, model: models.Model, dialect: Dialect = Dialect.MERMAID) -> None:
        """
        Initialize a model definition.

        Args:
            model: Django model class to represent
            dialect: ERD dialect for output formatting (default: Mermaid)
        """
        self.django_model = model
        self.dialect = dialect
        self.fields = self.django_model
        self.relationships = self.django_model
        self.name = model.__name__

    @property
    def fields(self) -> list[FieldDefinition]:
        """
        Get the list of field definitions for this model.

        Returns:
            List of FieldDefinition objects representing model fields
        """
        return self._fields

    @fields.setter
    def fields(self, model: models.Model) -> None:
        """
        Extract and process field definitions from the Django model.

        Processes all concrete fields from the model, creates FieldDefinition
        objects for each valid field, and sorts them with primary keys first.

        Args:
            model: Django model to extract fields from
        """
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
        """
        Get the relationship definitions for this model.

        Returns:
            RelationshipArray containing relationship definitions
        """
        return self._relationships

    @relationships.setter
    def relationships(self, django_model: models.Model) -> None:
        """
        Extract and process relationship definitions from the Django model.

        Processes all model fields to identify relationships (ForeignKey, ManyToMany, etc.)
        and creates relationship definitions. Excludes one_to_many relationships to avoid
        duplication with many_to_one relationships.

        Args:
            django_model: Django model to extract relationships from
        """
        valid_relationships = RelationshipArray(dialect=self.dialect)
        for field in django_model._meta.get_fields():
            relationship = FieldDefinition.get_relationship(field, dialect=self.dialect)
            if relationship and relationship.rel != "one_to_many":
                # NOTE: one_to_many and many_to_one are duplicated, so we only take one
                # of these values.
                valid_relationships.append(relationship)
        self._relationships = valid_relationships

    def to_string(self) -> str:
        """
        Generate string representation of the model in the specified dialect.

        Uses the appropriate pattern lookup for the dialect to format the model
        name and fields into the correct ERD syntax.

        Returns:
            String representation of the model in ERD dialect format
        """
        return MODEL_PATTERN_LOOKUP[self.dialect].format(
            model_name=self.django_model.__name__,
            model_fields=self.fields.to_string(),
        )


class ModelArray(BaseArray):
    """
    Collection of ModelDefinition objects for ERD generation.

    This class manages multiple Django models and provides methods to extract
    models from Django apps, process their relationships, and generate complete
    ERD representations. It handles deduplication of relationships and ensures
    consistent output formatting across different ERD dialects.

    Example:
        >>> models = ModelArray.get_models(['myapp'], dialect=Dialect.MERMAID)
        >>> print(models.to_string())
    """

    @classmethod
    def get_models(
        cls,
        valid_apps: Union[list[str], None] = None,
        dialect: Dialect = Dialect.MERMAID,
    ) -> "ModelArray":
        """
        Extract and create model definitions from Django apps.

        Retrieves all Django models from the specified apps (or all apps if none
        specified) and creates ModelDefinition objects for each model.

        Args:
            valid_apps: List of app labels to include, or None for all apps
            dialect: ERD dialect for output formatting

        Returns:
            ModelArray containing ModelDefinition objects for the specified models
        """
        _dialect = Dialect(dialect)
        valid = cls(dialect=_dialect)

        models = [i for i in d.apps.get_models()]
        for model in models:
            if not valid_apps or (model._meta.app_label in valid_apps):
                valid.append(ModelDefinition(model, dialect=_dialect))
        return valid

    @property
    def relationships(self) -> RelationshipArray:
        """
        Get deduplicated relationships across all models.

        Processes relationships from all models in the array and removes duplicates
        to ensure each relationship is represented only once in the ERD output.

        Returns:
            RelationshipArray containing unique relationship definitions
        """
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
        """
        Generate complete ERD representation for all models.

        Combines model definitions and relationships into a complete ERD
        using the appropriate output pattern for the specified dialect.

        Returns:
            Complete ERD string representation in the specified dialect format
        """
        models_string = "\n".join([i.to_string() for i in self])
        return OUTPUT_PATTERN_LOOKUP[self.dialect].format(
            models=models_string,
            relationships=self.relationships.to_string(),
        )

"""
Django relationship definitions for ERD generation.

This module provides classes for representing relationships between Django models
in various ERD dialects. It handles relationship type detection, field mapping,
and formatting relationship information according to different diagramming tools.
"""

from django.db import models

from django_erd_generator.contrib.dialects import (
    REL_CODE_LOOKUP,
    REL_PATTERN_LOOKUP,
    Dialect,
)
from django_erd_generator.definitions.base import BaseArray, BaseDefinition


class Relationship(BaseDefinition):
    """
    Represents a relationship between Django models for ERD generation.

    This class encapsulates relationships (ForeignKey, ManyToMany, OneToOne) between
    Django models and provides methods to format them according to different ERD
    dialects. It handles relationship direction, field mapping, and inverse relationships.

    Attributes:
        dialect: The ERD dialect for output formatting
        rel: The relationship type (one_to_many, many_to_one, etc.)
        from_model: Source model name in the relationship
        from_field: Source field name in the relationship
        to_model: Target model name in the relationship
        to_field: Target field name in the relationship

    Example:
        >>> field = Order._meta.get_field('customer')
        >>> rel = Relationship(field, 'many_to_one', dialect=Dialect.MERMAID)
        >>> print(rel.to_string())
    """

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
        """
        Initialize a relationship definition.

        Can be initialized either from a Django field (preferred) or by explicitly
        providing relationship details.

        Args:
            field: Django field representing the relationship (ForeignKey, etc.)
            rel_code: Relationship type code (one_to_many, many_to_one, etc.)
            dialect: ERD dialect for output formatting
            from_model: Source model name (used when field is None)
            from_field: Source field name (used when field is None)
            to_model: Target model name (used when field is None)
            to_field: Target field name (used when field is None)
        """
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
        """
        Create the inverse relationship.

        Generates the inverse relationship by swapping source and target models/fields
        and reversing the relationship type (e.g., one_to_many becomes many_to_one).

        Returns:
            Relationship object representing the inverse relationship
        """
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
        """
        Generate string representation of the relationship in the specified dialect.

        Uses the appropriate pattern lookup for the dialect to format the relationship
        information into the correct ERD syntax.

        Returns:
            String representation of the relationship in ERD dialect format
        """
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
    """
    Collection of Relationship objects.

    A specialized array for managing multiple relationship definitions with
    dialect-specific formatting capabilities. Inherits base functionality
    from BaseArray for consistent string generation across relationship collections.
    """

    pass

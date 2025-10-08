"""
Django field definitions for ERD generation.

This module provides classes for representing Django model fields in various ERD dialects.
It handles field type mapping, GIS field support, relationship detection, and formatting
field information according to different diagramming tool requirements.
"""

import re
from django.db import models, connection

from django_erd_generator.contrib.dialects import (
    FIELD_PATTERN_LOOKUP,
    PK_PATTERN_LOOKUP,
    Dialect,
)
from django_erd_generator.contrib.gis_fields import (
    is_gis_field,
    get_gis_field_type,
)
from django_erd_generator.definitions.base import BaseArray, BaseDefinition
from django_erd_generator.definitions.relationships import Relationship


class FieldDefinition(BaseDefinition):
    """
    Represents a single Django model field for ERD generation.

    This class encapsulates a Django model field and provides methods to extract
    and format field information according to different ERD dialects. It handles
    field type mapping, primary key detection, and special formatting requirements
    for different diagramming tools.

    Attributes:
        django_field: The Django field instance being represented
        dialect: The ERD dialect for output formatting
        col_name: The database column name for this field
        data_type: The field's data type information
        primary_key: Whether this field is a primary key

    Example:
        >>> field = MyModel._meta.get_field('name')
        >>> field_def = FieldDefinition(field, dialect=Dialect.MERMAID)
        >>> print(field_def.to_string())
    """

    def __init__(self, field: models.Field, dialect: Dialect = Dialect.MERMAID) -> None:
        """
        Initialize a field definition.

        Args:
            field: Django field instance to represent
            dialect: ERD dialect for output formatting (default: Mermaid)
        """
        self.django_field = field
        self.dialect = dialect
        self.col_name = self.django_field
        self.data_type = self.django_field
        self.primary_key = self.django_field

    @classmethod
    def get_relationship(
        cls,
        field: models.Field,
        dialect: Dialect = Dialect.MERMAID,
    ) -> Relationship:
        """
        Extract relationship information from a Django field.

        Analyzes a Django field to determine if it represents a relationship
        (ForeignKey, ManyToMany, etc.) and creates a Relationship object if found.

        Args:
            field: Django field to analyze for relationships
            dialect: ERD dialect for output formatting

        Returns:
            Relationship object if field is relational, None otherwise
        """
        rel_codes = ["one_to_many", "one_to_one", "many_to_one", "many_to_many"]
        if hasattr(field, "is_relation"):
            for rel_code in rel_codes:
                if getattr(field, rel_code, None):
                    return Relationship(field, rel_code, dialect=dialect)
        return None

    @classmethod
    def get_data_type(cls, field: models.Field, dialect: Dialect) -> dict:
        """
        Extract and format field data type information.

        Determines the appropriate data type representation for a Django field
        in the specified ERD dialect. Handles both regular Django fields and
        GIS fields, with special formatting rules for different dialects.

        Args:
            field: Django field to analyze
            dialect: ERD dialect for formatting requirements

        Returns:
            Dictionary with 'data_type' and 'args' keys, or None if type cannot be determined
        """
        # Check if it's a GIS field first
        field_class_name = field.__class__.__name__
        if is_gis_field(field_class_name):
            gis_type = get_gis_field_type(field_class_name, dialect)
            if gis_type:
                return {
                    "data_type": gis_type,
                    "args": None,
                }

        # Handle regular fields
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
        """
        Get the database column name for this field.

        Returns:
            String representing the database column name
        """
        return self._col_name

    @col_name.setter
    def col_name(self, field: models.Field) -> None:
        """
        Set the database column name from the Django field.

        Args:
            field: Django field to extract column name from
        """
        self._col_name = field.attname

    @property
    def data_type(self) -> dict:
        """
        Get the field data type information.

        Returns:
            Dictionary containing data type and arguments information
        """
        return self._data_type

    @data_type.setter
    def data_type(self, field: models.Field) -> None:
        """
        Set the data type information from the Django field.

        Args:
            field: Django field to extract data type from
        """
        self._data_type = self.get_data_type(field, self.dialect)

    @property
    def primary_key(self) -> bool:
        """
        Check if this field is a primary key.

        Returns:
            True if field is a primary key, False otherwise
        """
        return self._primary_key

    @primary_key.setter
    def primary_key(self, field: models.Field) -> None:
        """
        Set the primary key status from the Django field.

        Args:
            field: Django field to extract primary key status from
        """
        self._primary_key = field.primary_key

    def to_string(self) -> str:
        """
        Generate string representation of the field in the specified dialect.

        Uses the appropriate pattern lookup for the dialect to format the field
        information into the correct ERD syntax. Handles special formatting
        requirements for different dialects (e.g., PlantUML primary key notation).

        Returns:
            String representation of the field in ERD dialect format
        """
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
        """
        Return string representation of the field definition.

        Returns:
            String representation using to_string() method
        """
        return self.to_string()


class FieldArray(BaseArray):
    """
    Collection of FieldDefinition objects.

    A specialized array for managing multiple field definitions with
    dialect-specific formatting capabilities. Inherits base functionality
    from BaseArray for consistent string generation across field collections.
    """

    pass

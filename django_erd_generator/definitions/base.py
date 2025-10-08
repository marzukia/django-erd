"""
Base classes for ERD definition objects.

This module provides abstract base classes that define common functionality
for ERD generation components including string representation and collection
management with dialect-specific formatting.
"""

from django_erd_generator.contrib.dialects import Dialect


class BaseArray(list):
    """
    Base class for collections of definition objects.

    Extends Python's built-in list to provide ERD-specific functionality
    including dialect-aware string generation and consistent formatting
    across different definition collections.

    Attributes:
        dialect: The ERD dialect for output formatting
    """

    def __init__(self, dialect: Dialect = Dialect.MERMAID):
        """
        Initialize the array with a specific dialect.

        Args:
            dialect: ERD dialect for output formatting (default: Mermaid)
        """
        super().__init__()
        self.dialect = dialect

    def __repr__(self):
        """
        Return string representation of the array.

        Returns:
            String representation using to_string() method
        """
        return self.to_string()

    def to_string(self) -> str:
        """
        Generate string representation of all items in the array.

        Combines string representations of all contained definition objects,
        joining them with newlines for proper ERD formatting.

        Returns:
            Multi-line string with all items formatted for ERD output
        """
        return "\n".join(i.to_string() for i in self)


class BaseDefinition:
    """
    Base class for ERD definition objects.

    Provides common interface for all ERD definition classes including
    consistent string representation. All definition classes should
    inherit from this base and implement the to_string() method.
    """

    def __repr__(self):
        """
        Return string representation of the definition.

        Returns:
            String representation using to_string() method
        """
        return self.to_string()

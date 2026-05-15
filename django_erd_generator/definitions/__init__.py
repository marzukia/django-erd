"""Django ERD generator definitions package."""

from django_erd_generator.contrib.dialects import Dialect

# Default dialect for all definition classes
DEFAULT_DIALECT = Dialect.MERMAID

__all__ = ["Dialect", "DEFAULT_DIALECT"]

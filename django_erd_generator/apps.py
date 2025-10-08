"""
Django app configuration for ERD generator.

This module contains the Django app configuration for the ERD generator
package, defining app metadata and default settings.
"""

from django.apps import AppConfig


class DjangoErdConfig(AppConfig):
    """
    Django app configuration for the ERD generator.

    Configures the django_erd_generator Django application with
    appropriate settings for model field types and app identification.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_erd_generator"

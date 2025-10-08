"""
Django management command for generating data dictionaries.

This command extracts Django model information and generates comprehensive
Markdown documentation including field details, relationships, constraints,
and metadata. It's designed for creating technical documentation and
maintaining up-to-date schema information.
"""

from django.core.management.base import BaseCommand
from django_erd_generator.utils.data_dictionary import DataDictionary


class Command(BaseCommand):
    """
    Django management command to generate data dictionary documentation.

    This command analyzes Django models from specified apps and generates
    comprehensive Markdown documentation including:
    - Model field information and types
    - Relationship details and constraints
    - Primary keys, indexes, and validation rules
    - Help text and field descriptions
    - Table of contents with navigation links

    The output is structured by Django app and includes git version information
    for tracking documentation against code changes.

    Usage:
        python manage.py generate_data_dictionary [options]
    """

    help = "Generate a markdown data dictionary containing details of the models in one or more apps."

    def add_arguments(self, parser):
        """
        Add command line arguments for the data dictionary generation command.

        Args:
            parser: Django's argument parser for management commands
        """
        parser.add_argument(
            "-a",
            "--apps",
            required=False,
            default=None,
            help='The name of the apps which should be included in the data dictionary generated, these should be seperated by a comma, for example "shopping,polls". If no value is specified, all apps will be included.',
        )
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=None,
            help="The path to where the output of this content should be written, if no value is specified the output will be printed.",
        )

    def _parse_apps(self, apps: str) -> list[str] | None:
        """
        Parse the apps argument into a list of app names.

        Args:
            apps: Comma-separated string of app names

        Returns:
            List of app names, or None if no apps specified
        """
        if not apps:
            return None
        return [i.strip() for i in apps.split(",")]

    def handle(self, *args, **options):
        """
        Main command execution logic.

        Processes command arguments, generates data dictionary documentation
        from Django models, and outputs the result either to console or file.

        Args:
            *args: Positional arguments (unused)
            **options: Command options from argument parser
        """
        apps = self._parse_apps(options["apps"])
        output = options["output"]

        if output:
            DataDictionary.save_data_dictionary(apps=apps, path=output)
        else:
            print(DataDictionary.generate_data_dictionary(apps=apps))

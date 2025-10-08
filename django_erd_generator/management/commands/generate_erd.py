"""
Django management command for generating Entity-Relationship Diagrams.

This command extracts Django model information and generates ERD code
in various formats (Mermaid, PlantUML, dbdiagram.io) suitable for
different diagramming tools and documentation systems.
"""

from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.models import ModelArray

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Django management command to generate ERD syntax from Django models.

    This command analyzes Django models from specified apps and generates
    Entity-Relationship Diagram code in the chosen dialect format. It supports
    filtering by app and can output to console or file.

    Supported dialects:
    - mermaid: For GitHub/GitLab integration and web diagrams
    - plantuml: For detailed technical documentation
    - dbdiagram: For visual database design

    Usage:
        python manage.py generate_erd [options]
    """

    help = "For one or more apps generate the code to generate an ERD in the syntax of choice."

    def add_arguments(self, parser):
        """
        Add command line arguments for the ERD generation command.

        Args:
            parser: Django's argument parser for management commands
        """
        parser.add_argument(
            "-a",
            "--apps",
            required=False,
            default=None,
            help='The name of the apps which should be included in the ERD generated, these should be seperated by a comma, for example "shopping,polls". If no value is specified, all apps will be included.',
        )
        parser.add_argument(
            "-d",
            "--dialect",
            required=False,
            default="mermaid",
            help="The dialect which should be used, it should be either 'mermaid', 'plantuml' or 'dbdiagram'.",
        )
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default=None,
            help="The path to where the output of this content should be written, if no value is specified the output will be printed.",
        )

    def _parse_dialect(self, dialect: str) -> Dialect:
        """
        Parse and validate the dialect argument.

        Args:
            dialect: String name of the dialect to use

        Returns:
            Dialect enum value

        Raises:
            CommandError: If dialect is not supported
        """
        valid = [i.value for i in Dialect]
        if dialect not in valid:
            valid_string = ", ".join(valid)
            err = f"{dialect} is not a valid choice, must be {valid_string}"
            raise CommandError(err)
        return Dialect(dialect)

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

    def _write_output(
        self,
        output_destination: str,
        output_content: ModelArray,
    ) -> None:
        """
        Write ERD content to a file.

        Args:
            output_destination: Path to the output file
            output_content: ModelArray containing the ERD data
        """
        with open(output_destination, "w") as dst:
            dst.write(output_content.to_string())

    def handle(self, *args, **options):
        """
        Main command execution logic.

        Processes command arguments, generates ERD data from Django models,
        and outputs the result either to console or file.

        Args:
            *args: Positional arguments (unused)
            **options: Command options from argument parser
        """
        dialect = self._parse_dialect(options["dialect"])
        apps = self._parse_apps(options["apps"])
        output = options["output"]
        erd = ModelArray.get_models(apps, dialect=dialect)
        if output:
            self._write_output(output, erd)
        else:
            print(erd.to_string())

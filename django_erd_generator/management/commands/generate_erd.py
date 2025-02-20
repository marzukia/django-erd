from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.models import ModelArray

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "For one or more apps generate the code to generate an ERD in the syntax of choice."

    def add_arguments(self, parser):
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
        valid = [i.value for i in Dialect]
        if dialect not in valid:
            valid_string = ", ".join(valid)
            err = f"{dialect} is not a valid choice, must be {valid_string}"
            raise CommandError(err)
        return Dialect(dialect)

    def _parse_apps(self, apps: str) -> list[str] | None:
        if not apps:
            return None
        return [i.strip() for i in apps.split(",")]

    def _write_output(
        self,
        output_destination: str,
        output_content: ModelArray,
    ) -> None:
        with open(output_destination, "w") as dst:
            dst.write(output_content.to_string())

    def handle(self, *args, **options):
        dialect = self._parse_dialect(options["dialect"])
        apps = self._parse_apps(options["apps"])
        output = options["output"]
        erd = ModelArray.get_models(apps, dialect=dialect)
        if output:
            self._write_output(output, erd)
        else:
            print(erd.to_string())

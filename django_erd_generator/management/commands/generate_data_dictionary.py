from django.core.management.base import BaseCommand
from django_erd_generator.utils.data_dictionary import DataDictionary


class Command(BaseCommand):
    help = "Generate a markdown data dictionary containing details of the models in one or more apps."

    def add_arguments(self, parser):
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
        if not apps:
            return None
        return [i.strip() for i in apps.split(",")]

    def handle(self, *args, **options):
        apps = self._parse_apps(options["apps"])
        output = options["output"]

        if output:
            DataDictionary.save_data_dictionary(apps=apps, path=output)
        else:
            print(DataDictionary.get_data_dictionary(apps=apps))

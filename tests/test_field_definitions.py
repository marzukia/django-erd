from unittest import TestCase

from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.fields import FieldDefinition
from .models import Customer
from .utils import ModelArray


class FieldTestCase(TestCase):
    def test_init_field_definition(self):
        field = Customer._meta.get_field("id")
        field_definition = FieldDefinition(field)
        self.assertEqual(field_definition.col_name, "id")
        self.assertEqual(field_definition.data_type["data_type"], "integer")
        self.assertEqual(field_definition.primary_key, True)

    def test_field_definition_dialect_render(self):
        field = Customer._meta.get_field("id")

        dialects = {
            Dialect.MERMAID: "integer id pk",
            Dialect.PLANTUML: "*id: integer",
            Dialect.DBDIAGRAM: 'id "integer" [primary key]',
        }

        for dialect, expected in dialects.items():
            field_definition = FieldDefinition(field, dialect=dialect)
            self.assertEqual(expected, field_definition.to_string().strip())


class FieldArrayTestCase(TestCase):
    def test_field_array_dialect_render(self):
        dialects = {
            Dialect.MERMAID: [
                "integer id pk",
                "text first_name",
                "text last_name",
            ],
            Dialect.PLANTUML: [
                "*id: integer",
                "first_name: text",
                "last_name: text",
            ],
            Dialect.DBDIAGRAM: [
                'id "integer" [primary key]',
                'first_name "text"',
                'last_name "text"',
            ],
        }

        for dialect, expected in dialects.items():
            model = ModelArray.get_models("tests", dialect=dialect)[0]
            fields = model.fields.to_string()
            field_arr = [i.strip() for i in fields.split("\n")]
            self.assertEqual(" ".join(field_arr), " ".join(expected))

import os
from unittest import TestCase

from django_erd_generator.contrib.dialects import Dialect
from .utils import ModelArray


class ModelDefinitionTestCase(TestCase):
    def setUp(self):
        self.models = ModelArray.get_models("tests")

    def test_field_names(self):
        expected_fields = [
            ["id", "first_name", "last_name"],
            ["id", "sku", "product_name", "product_code", "quantity", "price"],
            ["id", "customer_id", "product_id", "quantity", "order_total"],
            ["id", "name", "label"],
        ]
        for i, model in enumerate(self.models):
            field_names = [x.col_name for x in model.fields]
            names_exist = all([x in field_names for x in expected_fields[i]])
            self.assertEqual(names_exist, True)

    def test_field_types(self):
        expected_types = [
            ["integer", "text", "text"],
            ["integer", "text", "text", "integer", "decimal"],
            ["integer", "integer", "integer", "integer", "decimal"],
            ["integer", "text", "text"],
        ]
        for i, model in enumerate(self.models):
            field_types = [x.data_type["data_type"] for x in model.fields]
            types_correct = all([x in field_types for x in expected_types[i]])
            self.assertEqual(types_correct, True)

    def test_model_relationships(self):
        expected_relationships = {
            1: [
                ("Product", "Region", "many_to_many"),
            ],
            2: [
                ("Order", "Customer", "many_to_one"),
                ("Order", "Product", "many_to_one"),
            ],
        }
        for i, relationships in expected_relationships.items():
            target = self.models[i].relationships
            for j, (to_model, from_model, rel) in enumerate(relationships):
                self.assertEqual(target[j].from_model, from_model)
                self.assertEqual(target[j].to_model, to_model)
                self.assertEqual(target[j].rel, rel)


class ModelArrayTestCase(TestCase):
    def setUp(self):
        self._ = ModelArray.get_models("test")
        self.maxDiff = None

    def test_array_relationships(self):
        relationships = self._.relationships
        expected_relationships = [
            ("Product", "Region", "many_to_many"),
            ("Order", "Customer", "many_to_one"),
            ("Order", "Product", "many_to_one"),
        ]

        for i, (to_model, from_model, rel) in enumerate(expected_relationships):
            self.assertEqual(relationships[i].from_model, from_model)
            self.assertEqual(relationships[i].to_model, to_model)
            self.assertEqual(relationships[i].rel, rel)

    def test_model_array_dialect_render(self):
        test_dir = os.path.dirname(__file__)
        test_data = os.path.join(test_dir, "test_data")
        expected_render = {
            Dialect.MERMAID: open(os.path.join(test_data, "mermaid.txt")).read(),
            Dialect.PLANTUML: open(os.path.join(test_data, "plantuml.txt")).read(),
            Dialect.DBDIAGRAM: open(os.path.join(test_data, "dbdiagram.txt")).read(),
        }
        for dialect, expected in expected_render.items():
            model_arr = ModelArray.get_models("test", dialect=dialect)
            self.assertEqual(model_arr.to_string(), expected)

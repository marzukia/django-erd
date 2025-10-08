from unittest import TestCase

from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.fields import Relationship
from .models import Order
from .utils import ModelArray


class RelationshipTestCase(TestCase):
    def test_init_relationship_definition(self):
        field = Order._meta.get_field("customer")
        relationship = Relationship(field, "one_to_many")
        self.assertEqual(relationship.to_model, "Order")
        self.assertEqual(relationship.from_model, "Customer")
        self.assertEqual(relationship.rel, "one_to_many")

    def test_relationship_definition_dialect_render(self):
        field = Order._meta.get_field("customer")

        dialects = {
            Dialect.MERMAID: 'Order ||--|{ Customer: ""',
            Dialect.PLANTUML: "Order ||--|{ Customer",
            Dialect.DBDIAGRAM: "Ref: Order.customer_id < Customer.id",
        }

        for dialect, expected in dialects.items():
            rel_definition = Relationship(field, "one_to_many", dialect=dialect)
            self.assertEqual(expected, rel_definition.to_string().strip())


class RelationshipArrayTestCase(TestCase):
    def test_relationship_array_dialect_render(self):
        dialects = {
            Dialect.MERMAID: 'Order }|--|| Customer: ""\nOrder }|--|| Product: ""',
            Dialect.PLANTUML: "Order }|--|| Customer\nOrder }|--|| Product",
            Dialect.DBDIAGRAM: "Ref: Order.customer_id > Customer.id\nRef: Order.product_id > Product.id",
        }

        for dialect, expected in dialects.items():
            model = ModelArray.get_models("tests", dialect=dialect)[2]
            relationships = model.relationships.to_string()
            self.assertEqual(relationships, expected)

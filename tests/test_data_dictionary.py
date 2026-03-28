"""
Test cases for data dictionary functionality in Django ERD Generator.
"""

from unittest import TestCase
from django_erd_generator.utils.data_dictionary import DataDictionary
from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.definitions.models import ModelDefinition
from django_erd_generator.definitions.fields import FieldDefinition
from .models import Customer, Product, Order, Region, TaggedItem


class DataDictionaryTestCase(TestCase):
    """Test data dictionary generation functionality."""

    def test_data_dictionary_creation(self):
        """Test that data dictionaries can be created."""
        # Test that we can create a data dictionary
        try:
            dict_obj = DataDictionary()
            self.assertIsNotNone(dict_obj)
        except Exception as e:
            self.fail(f"DataDictionary creation failed: {e}")

    def test_model_data_dictionary_generation(self):
        """Test data dictionary generation for individual models."""
        # Test Customer model
        customer_def = ModelDefinition(Customer, dialect=Dialect.MERMAID)
        customer_dict = DataDictionary.render_model(customer_def)

        self.assertIsNotNone(customer_dict)
        self.assertTrue(len(customer_dict) > 0)

        # Should contain model name
        self.assertIn("Customer", customer_dict)

        # Should contain field information
        self.assertIn("id", customer_dict)
        self.assertIn("first_name", customer_dict)
        self.assertIn("last_name", customer_dict)

    def test_multiple_model_data_dictionary(self):
        """Test data dictionary generation for multiple models."""
        # Test with all models
        models = [Customer, Product, Order, Region]
        all_dicts = []

        for model in models:
            model_def = ModelDefinition(model, dialect=Dialect.MERMAID)
            model_dict = DataDictionary.render_model(model_def)
            all_dicts.append(model_dict)
            self.assertIsNotNone(model_dict)
            self.assertTrue(len(model_dict) > 0)

    def test_data_dictionary_formatting(self):
        """Test that data dictionary formatting works correctly."""
        customer_def = ModelDefinition(Customer, dialect=Dialect.MERMAID)
        customer_dict = DataDictionary.render_model(customer_def)

        # Should be a string
        self.assertIsInstance(customer_dict, str)

        # Should contain expected elements
        self.assertIn("## Customer", customer_dict)
        self.assertIn("id", customer_dict)
        self.assertIn("first_name", customer_dict)
        self.assertIn("last_name", customer_dict)

    def test_data_dictionary_with_different_dialects(self):
        """Test data dictionary generation with different dialects."""
        customer_def = ModelDefinition(Customer, dialect=Dialect.MERMAID)
        mermaid_dict = DataDictionary.render_model(customer_def)

        customer_def_plantuml = ModelDefinition(Customer, dialect=Dialect.PLANTUML)
        plantuml_dict = DataDictionary.render_model(customer_def_plantuml)

        customer_def_dbdiagram = ModelDefinition(Customer, dialect=Dialect.DBDIAGRAM)
        dbdiagram_dict = DataDictionary.render_model(customer_def_dbdiagram)

        # All should be non-empty
        self.assertIsNotNone(mermaid_dict)
        self.assertIsNotNone(plantuml_dict)
        self.assertIsNotNone(dbdiagram_dict)

        # They should all contain the same basic information but in different formats
        self.assertIn("Customer", mermaid_dict)
        self.assertIn("Customer", plantuml_dict)
        self.assertIn("Customer", dbdiagram_dict)

    def test_empty_data_dictionary(self):
        """Test data dictionary generation with minimal models."""
        # Test that we can handle models with minimal fields
        try:
            # Create a minimal model definition
            minimal_model = ModelDefinition(Customer, dialect=Dialect.MERMAID)
            minimal_dict = DataDictionary.render_model(minimal_model)
            self.assertIsNotNone(minimal_dict)
        except Exception as e:
            self.fail(f"Empty data dictionary test failed: {e}")

    def test_related_model_handling(self):
        """Test that related model handling works correctly, especially edge cases."""
        # Test with Order model which has ForeignKey relationships
        order_def = ModelDefinition(Order, dialect=Dialect.MERMAID)
        order_dict = DataDictionary.render_model(order_def)

        self.assertIsNotNone(order_dict)
        self.assertTrue(len(order_dict) > 0)

        # Should contain references to related models
        self.assertIn("Customer", order_dict)  # Customer is related via ForeignKey
        self.assertIn("Product", order_dict)  # Product is related via ForeignKey

        # Check that the related model references are properly formatted
        # This tests the fix for the bug in related_model handling
        self.assertIn("[Customer](#Customer)", order_dict)
        self.assertIn("[Product](#Product)", order_dict)

    def test_self_referential_model(self):
        """Test data dictionary generation for models with self-referential relationships."""
        # Create a model with self-reference
        from django.db import models

        class SelfReferencingModel(models.Model):
            name = models.TextField()
            parent = models.ForeignKey(
                "self", on_delete=models.CASCADE, null=True, blank=True
            )

            class Meta:
                app_label = "tests"

        # Test that we can generate dictionary for self-referencing model
        try:
            model_def = ModelDefinition(SelfReferencingModel, dialect=Dialect.MERMAID)
            model_dict = DataDictionary.render_model(model_def)
            self.assertIsNotNone(model_dict)
            self.assertTrue(len(model_dict) > 0)
        except Exception as e:
            self.fail(f"Self-referential model test failed: {e}")

    def test_generic_foreign_key_handling(self):
        """Test data dictionary generation with GenericForeignKey fields."""
        # Test TaggedItem model which has GenericForeignKey
        tagged_item_def = ModelDefinition(TaggedItem, dialect=Dialect.MERMAID)
        tagged_item_dict = DataDictionary.render_model(tagged_item_def)

        self.assertIsNotNone(tagged_item_dict)
        self.assertTrue(len(tagged_item_dict) > 0)

        # Should contain references to related models
        self.assertIn("ContentType", tagged_item_dict)

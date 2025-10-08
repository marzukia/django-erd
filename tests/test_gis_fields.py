"""
Test cases for GIS field support in ERD generation.
"""

import unittest
from unittest import TestCase

from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.contrib.gis_fields import (
    is_gis_field,
    get_gis_field_type,
)
from django_erd_generator.definitions.fields import FieldDefinition

# Import test models
try:
    from .gis_models import TestGISModel, TestLocationModel, GIS_AVAILABLE
except ImportError:
    GIS_AVAILABLE = False


class GISFieldTestCase(TestCase):
    """Test GIS field type detection and mapping."""

    def test_is_gis_field_detection(self):
        """Test that GIS fields are correctly identified."""
        # Test positive cases
        self.assertTrue(is_gis_field("PointField"))
        self.assertTrue(is_gis_field("PolygonField"))
        self.assertTrue(is_gis_field("LineStringField"))
        self.assertTrue(is_gis_field("MultiPointField"))
        self.assertTrue(is_gis_field("MultiLineStringField"))
        self.assertTrue(is_gis_field("MultiPolygonField"))
        self.assertTrue(is_gis_field("GeometryCollectionField"))
        self.assertTrue(is_gis_field("GeometryField"))
        self.assertTrue(is_gis_field("RasterField"))

        # Test negative cases
        self.assertFalse(is_gis_field("CharField"))
        self.assertFalse(is_gis_field("IntegerField"))
        self.assertFalse(is_gis_field("TextField"))
        self.assertFalse(is_gis_field("ForeignKey"))

    def test_gis_field_type_mapping(self):
        """Test that GIS field types are correctly mapped for different dialects."""
        test_cases = [
            ("PointField", Dialect.MERMAID, "geometry_point"),
            ("PointField", Dialect.PLANTUML, "POINT"),
            ("PointField", Dialect.DBDIAGRAM, "geometry(POINT)"),
            ("PolygonField", Dialect.MERMAID, "geometry_polygon"),
            ("PolygonField", Dialect.PLANTUML, "POLYGON"),
            ("PolygonField", Dialect.DBDIAGRAM, "geometry(POLYGON)"),
            ("GeometryField", Dialect.MERMAID, "geometry"),
            ("GeometryField", Dialect.PLANTUML, "GEOMETRY"),
            ("GeometryField", Dialect.DBDIAGRAM, "geometry"),
        ]

        for field_name, dialect, expected_type in test_cases:
            with self.subTest(field=field_name, dialect=dialect):
                result = get_gis_field_type(field_name, dialect)
                self.assertEqual(result, expected_type)

    def test_non_gis_field_returns_none(self):
        """Test that non-GIS fields return None."""
        result = get_gis_field_type("CharField", Dialect.MERMAID)
        self.assertIsNone(result)


@unittest.skipUnless(GIS_AVAILABLE, "Django GIS not available")
class GISFieldDefinitionTestCase(TestCase):
    """Test GIS field definition rendering."""

    def test_gis_field_definition_creation(self):
        """Test that GIS field definitions are created correctly."""
        location_field = TestGISModel._meta.get_field("location")
        field_def = FieldDefinition(location_field, dialect=Dialect.MERMAID)

        self.assertEqual(field_def.col_name, "location")
        self.assertEqual(field_def.data_type["data_type"], "geometry_point")
        self.assertFalse(field_def.primary_key)

    def test_gis_field_dialect_rendering(self):
        """Test that GIS fields render correctly for different dialects."""
        location_field = TestGISModel._meta.get_field("location")

        dialects_expected = {
            Dialect.MERMAID: "geometry_point location",
            Dialect.PLANTUML: "location: POINT",
            Dialect.DBDIAGRAM: 'location "geometry(POINT)"',
        }

        for dialect, expected in dialects_expected.items():
            with self.subTest(dialect=dialect):
                field_def = FieldDefinition(location_field, dialect=dialect)
                result = field_def.to_string().strip()
                self.assertEqual(result, expected)

    def test_polygon_field_rendering(self):
        """Test polygon field rendering."""
        boundary_field = TestGISModel._meta.get_field("boundary")

        dialects_expected = {
            Dialect.MERMAID: "geometry_polygon boundary",
            Dialect.PLANTUML: "boundary: POLYGON",
            Dialect.DBDIAGRAM: 'boundary "geometry(POLYGON)"',
        }

        for dialect, expected in dialects_expected.items():
            with self.subTest(dialect=dialect):
                field_def = FieldDefinition(boundary_field, dialect=dialect)
                result = field_def.to_string().strip()
                self.assertEqual(result, expected)


@unittest.skipUnless(GIS_AVAILABLE, "Django GIS not available")
class GISModelGenerationTestCase(TestCase):
    """Test full model generation with GIS fields."""

    def test_model_with_gis_fields_mermaid(self):
        """Test complete model generation with GIS fields for Mermaid."""
        from django_erd_generator.definitions.models import ModelDefinition

        model_def = ModelDefinition(TestLocationModel, dialect=Dialect.MERMAID)
        result = model_def.to_string()

        # Check that the model structure is correct
        self.assertIn("TestLocationModel", result)
        self.assertIn("text name", result)
        self.assertIn("geometry_point coordinates", result)
        self.assertIn("geometry_polygon coverage_area", result)

    def test_model_with_gis_fields_plantuml(self):
        """Test complete model generation with GIS fields for PlantUML."""
        from django_erd_generator.definitions.models import ModelDefinition

        model_def = ModelDefinition(TestLocationModel, dialect=Dialect.PLANTUML)
        result = model_def.to_string()

        # Check that the model structure is correct
        self.assertIn("entity TestLocationModel", result)
        self.assertIn("name: text", result)
        self.assertIn("coordinates: POINT", result)
        self.assertIn("coverage_area: POLYGON", result)

    def test_model_with_gis_fields_dbdiagram(self):
        """Test complete model generation with GIS fields for dbdiagram."""
        from django_erd_generator.definitions.models import ModelDefinition

        model_def = ModelDefinition(TestLocationModel, dialect=Dialect.DBDIAGRAM)
        result = model_def.to_string()

        # Check that the model structure is correct
        self.assertIn("Table TestLocationModel", result)
        self.assertIn('name "text"', result)
        self.assertIn('coordinates "geometry(POINT)"', result)
        self.assertIn('coverage_area "geometry(POLYGON)"', result)

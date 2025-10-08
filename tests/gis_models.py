"""
Test models for GIS field support.
"""

from django.db import models

# Try to import GIS fields, fallback gracefully if not available
try:
    from django.contrib.gis.db import models as gis_models

    GIS_AVAILABLE = True
except ImportError:
    GIS_AVAILABLE = False

    # Create dummy classes for testing when GIS is not available
    class DummyGISField(models.Field):
        pass

    gis_models = type(
        "gis_models",
        (),
        {
            "PointField": DummyGISField,
            "PolygonField": DummyGISField,
            "LineStringField": DummyGISField,
            "MultiPointField": DummyGISField,
            "MultiLineStringField": DummyGISField,
            "MultiPolygonField": DummyGISField,
            "GeometryCollectionField": DummyGISField,
            "GeometryField": DummyGISField,
            "RasterField": DummyGISField,
        },
    )


class TestGISModel(models.Model):
    """Test model with various GIS field types."""

    name = models.CharField(max_length=100)

    # Basic geometry fields
    location = gis_models.PointField(help_text="Store location as a point")
    boundary = gis_models.PolygonField(help_text="Store boundary as a polygon")
    route = gis_models.LineStringField(help_text="Store route as a line")

    # Multi-geometry fields
    locations = gis_models.MultiPointField(null=True, blank=True)
    boundaries = gis_models.MultiPolygonField(null=True, blank=True)
    routes = gis_models.MultiLineStringField(null=True, blank=True)

    # Generic geometry field
    any_geometry = gis_models.GeometryField(null=True, blank=True)

    # Geometry collection
    mixed_geometry = gis_models.GeometryCollectionField(null=True, blank=True)

    class Meta:
        app_label = "tests"


class TestLocationModel(models.Model):
    """Simple location model for testing."""

    name = models.CharField(max_length=50)
    coordinates = gis_models.PointField()
    coverage_area = gis_models.PolygonField(null=True, blank=True)

    class Meta:
        app_label = "tests"

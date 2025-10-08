"""
GIS field type mappings for different ERD dialects.

This module provides support for Django's GeoDjango (GIS) fields in ERD generation.
It maps Django GIS field types to appropriate representations in different ERD
dialects, ensuring that spatial/geographic fields are properly represented in
database diagrams.

Supported GIS Fields:
- PointField: Geographic points (latitude/longitude)
- LineStringField: Geographic lines/paths
- PolygonField: Geographic areas/regions
- MultiPointField: Collections of points
- MultiLineStringField: Collections of lines
- MultiPolygonField: Collections of polygons
- GeometryCollectionField: Mixed geometry collections
- GeometryField: Generic geometry field
- RasterField: Raster/image data
"""

from django_erd_generator.contrib.dialects import Dialect

# GIS field type mappings for different dialects
GIS_FIELD_TYPE_MAPPING = {
    Dialect.MERMAID: {
        "PointField": "geometry_point",
        "LineStringField": "geometry_linestring",
        "PolygonField": "geometry_polygon",
        "MultiPointField": "geometry_multipoint",
        "MultiLineStringField": "geometry_multilinestring",
        "MultiPolygonField": "geometry_multipolygon",
        "GeometryCollectionField": "geometry_collection",
        "GeometryField": "geometry",
        "RasterField": "raster",
    },
    Dialect.PLANTUML: {
        "PointField": "POINT",
        "LineStringField": "LINESTRING",
        "PolygonField": "POLYGON",
        "MultiPointField": "MULTIPOINT",
        "MultiLineStringField": "MULTILINESTRING",
        "MultiPolygonField": "MULTIPOLYGON",
        "GeometryCollectionField": "GEOMETRYCOLLECTION",
        "GeometryField": "GEOMETRY",
        "RasterField": "RASTER",
    },
    Dialect.DBDIAGRAM: {
        "PointField": "geometry(POINT)",
        "LineStringField": "geometry(LINESTRING)",
        "PolygonField": "geometry(POLYGON)",
        "MultiPointField": "geometry(MULTIPOINT)",
        "MultiLineStringField": "geometry(MULTILINESTRING)",
        "MultiPolygonField": "geometry(MULTIPOLYGON)",
        "GeometryCollectionField": "geometry(GEOMETRYCOLLECTION)",
        "GeometryField": "geometry",
        "RasterField": "raster",
    },
    Dialect.MERMAID_FLOW: {
        "PointField": "point",
        "LineStringField": "linestring",
        "PolygonField": "polygon",
        "MultiPointField": "multipoint",
        "MultiLineStringField": "multilinestring",
        "MultiPolygonField": "multipolygon",
        "GeometryCollectionField": "geometry_collection",
        "GeometryField": "geometry",
        "RasterField": "raster",
    },
}


def is_gis_field(field_class_name: str) -> bool:
    """
    Check if a field is a GIS field based on its class name.

    Determines whether a Django field is a geographic/spatial field type
    by checking its class name against known GIS field types.

    Args:
        field_class_name: The name of the field class (e.g., 'PointField')

    Returns:
        True if the field is a GIS field, False otherwise

    Example:
        >>> is_gis_field('PointField')
        True
        >>> is_gis_field('CharField')
        False
    """
    gis_field_names = {
        "PointField",
        "LineStringField",
        "PolygonField",
        "MultiPointField",
        "MultiLineStringField",
        "MultiPolygonField",
        "GeometryCollectionField",
        "GeometryField",
        "RasterField",
    }
    return field_class_name in gis_field_names


def get_gis_field_type(field_class_name: str, dialect: Dialect) -> str:
    """
    Get the appropriate GIS field type representation for the given dialect.

    Maps a Django GIS field class name to its appropriate representation
    in the specified ERD dialect. Different dialects have different
    conventions for representing spatial data types.

    Args:
        field_class_name: The name of the GIS field class
        dialect: The ERD dialect for output formatting

    Returns:
        String representation of the field type in the dialect, or None if
        not a GIS field

    Example:
        >>> get_gis_field_type('PointField', Dialect.MERMAID)
        'geometry_point'
        >>> get_gis_field_type('PointField', Dialect.PLANTUML)
        'POINT'
        >>> get_gis_field_type('CharField', Dialect.MERMAID)
        None
    """
    if not is_gis_field(field_class_name):
        return None

    mapping = GIS_FIELD_TYPE_MAPPING.get(dialect, {})
    return mapping.get(field_class_name, "geometry")

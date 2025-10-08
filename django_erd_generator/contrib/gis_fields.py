"""
GIS field type mappings for different dialects.
Maps Django GIS field types to appropriate representations in ERD dialects.
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
    """Check if a field is a GIS field based on its class name."""
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
    """Get the appropriate GIS field type for the given dialect."""
    if not is_gis_field(field_class_name):
        return None

    mapping = GIS_FIELD_TYPE_MAPPING.get(dialect, {})
    return mapping.get(field_class_name, "geometry")

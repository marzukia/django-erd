"""
ERD dialect definitions and formatting patterns.

This module defines the supported ERD dialects and their corresponding formatting
patterns for models, fields, relationships, and output structures. It provides
lookup tables for converting Django model information into the appropriate
syntax for different diagramming tools.

Supported Dialects:
- Mermaid: For GitHub/GitLab integration and web-based diagrams
- PlantUML: For detailed technical documentation
- dbdiagram.io: For visual database design
- Mermaid Flow: Alternative Mermaid format for flowcharts
"""

from enum import Enum


class Dialect(Enum):
    """
    Enumeration of supported ERD dialects.

    Each dialect represents a different diagramming tool or format with
    specific syntax requirements for representing database schemas.
    """

    MERMAID = "mermaid"
    PLANTUML = "plantuml"
    DBDIAGRAM = "dbdiagram"
    MERMAID_FLOW = "mermaid_flow"


# Relationship code mappings for different dialects
REL_CODE_LOOKUP = {
    Dialect.MERMAID: {
        "one_to_many": "||--|{",
        "one_to_one": "||--||",
        "many_to_one": "}|--||",
        "many_to_many": "}|--|{",
    },
    Dialect.PLANTUML: {
        "one_to_many": "||--|{",
        "one_to_one": "||--||",
        "many_to_one": "}|--||",
        "many_to_many": "}|--|{",
    },
    Dialect.DBDIAGRAM: {
        "one_to_many": "<",
        "one_to_one": "-",
        "many_to_one": ">",
        "many_to_many": "<>",
    },
    Dialect.MERMAID_FLOW: {
        "one_to_many": "o--x",
        "one_to_one": "o--o",
        "many_to_one": "x--o",
        "many_to_many": "x--x",
    },
}

# Relationship formatting patterns for different dialects
REL_PATTERN_LOOKUP = {
    Dialect.MERMAID: '{to_model} {rel_code} {from_model}: ""',
    Dialect.MERMAID_FLOW: "{to_model} {rel_code} {from_model}",
    Dialect.DBDIAGRAM: "Ref: {to_model}.{to_field} {rel_code} {from_model}.{from_field}",
    Dialect.PLANTUML: "{to_model} {rel_code} {from_model}",
}

# Field formatting patterns for different dialects
FIELD_PATTERN_LOOKUP = {
    Dialect.MERMAID: "  {data_type} {col_name} {primary_key}",
    Dialect.MERMAID_FLOW: "",
    Dialect.DBDIAGRAM: '  {col_name} "{data_type}" {primary_key}',
    Dialect.PLANTUML: "  {col_name}: {data_type}",
}

# Primary key indicators for different dialects
PK_PATTERN_LOOKUP = {
    Dialect.MERMAID: "pk",
    Dialect.MERMAID_FLOW: None,
    Dialect.DBDIAGRAM: "[primary key]",
    Dialect.PLANTUML: None,
}

# Model structure patterns for different dialects
MODEL_PATTERN_LOOKUP = {
    Dialect.MERMAID: "{model_name} {{\n{model_fields}\n}}",
    Dialect.MERMAID_FLOW: "{model_name}",
    Dialect.DBDIAGRAM: "Table {model_name} {{\n{model_fields}\n}}",
    Dialect.PLANTUML: "entity {model_name} {{\n{model_fields}\n}}",
}

# Complete output structure patterns for different dialects
OUTPUT_PATTERN_LOOKUP = {
    Dialect.MERMAID: "erDiagram\n{models}\n{relationships}",
    Dialect.MERMAID_FLOW: "flowchart\n{models}\n{relationships}",
    Dialect.DBDIAGRAM: "{models}\n{relationships}",
    Dialect.PLANTUML: "@startuml\n\n{models}\n{relationships}\n\n@enduml",
}

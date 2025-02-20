from enum import Enum


class Dialect(Enum):
    MERMAID = "mermaid"
    PLANTUML = "plantuml"
    DBDIAGRAM = "dbdiagram"
    MERMAID_FLOW = "mermaid_flow"


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

REL_PATTERN_LOOKUP = {
    Dialect.MERMAID: '{to_model} {rel_code} {from_model}: ""',
    Dialect.MERMAID_FLOW: "{to_model} {rel_code} {from_model}",
    Dialect.DBDIAGRAM: "Ref: {to_model}.{to_field} {rel_code} {from_model}.{from_field}",
    Dialect.PLANTUML: "{to_model} {rel_code} {from_model}",
}

FIELD_PATTERN_LOOKUP = {
    Dialect.MERMAID: "  {data_type} {col_name} {primary_key}",
    Dialect.MERMAID_FLOW: "",
    Dialect.DBDIAGRAM: '  {col_name} "{data_type}" {primary_key}',
    Dialect.PLANTUML: "  {col_name}: {data_type}",
}

PK_PATTERN_LOOKUP = {
    Dialect.MERMAID: "pk",
    Dialect.MERMAID_FLOW: None,
    Dialect.DBDIAGRAM: "[primary key]",
    Dialect.PLANTUML: None,
}

MODEL_PATTERN_LOOKUP = {
    Dialect.MERMAID: "{model_name} {{\n{model_fields}\n}}",
    Dialect.MERMAID_FLOW: "{model_name}",
    Dialect.DBDIAGRAM: "Table {model_name} {{\n{model_fields}\n}}",
    Dialect.PLANTUML: "entity {model_name} {{\n{model_fields}\n}}",
}

OUTPUT_PATTERN_LOOKUP = {
    Dialect.MERMAID: "erDiagram\n{models}\n{relationships}",
    Dialect.MERMAID_FLOW: "flowchart\n{models}\n{relationships}",
    Dialect.DBDIAGRAM: "{models}\n{relationships}",
    Dialect.PLANTUML: "@startuml\n\n{models}\n{relationships}\n\n@enduml",
}

from django_erd_generator.contrib.dialects import Dialect


class BaseArray(list):
    def __init__(self, dialect: Dialect = Dialect.MERMAID):
        super().__init__()
        self.dialect = dialect

    def __repr__(self):
        return self.to_string()

    def to_string(self) -> str:
        return "\n".join(i.to_string() for i in self)


class BaseDefinition:
    def __repr__(self):
        return self.to_string()

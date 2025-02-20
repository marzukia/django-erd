import csv
from django_erd.contrib.dialects import Dialect
from django_erd.definitions.models import ModelArray

erd = ModelArray.get_models(["propertyflow"], dialect=Dialect.PLANTUML)

rows = []
for model in erd:
    for field in model.fields:
        django_field = field.django_field
        row = (
            model.name,
            django_field.verbose_name,
            field.col_name,
            field.data_type["data_type"],
            django_field.help_text,
        )
        rows.append(row)

headers = ["data_model", "column_name", "db_column", "data_type", "description"]

with open("./data_dictionary.csv", "w") as dst:
    writer = csv.writer(dst)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

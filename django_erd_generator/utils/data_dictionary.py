from collections import defaultdict
import os
from typing import Dict, List, Optional
from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.contrib.markdown import Table
from django_erd_generator.definitions.models import ModelArray, ModelDefinition
from django_erd_generator.utils.git import get_git_commit

MODEL_RENDER_TEMPLATE = """\
#### {model_name}

`{signature}`

{doc_string}

{table}
"""

APPS_RENDER_TEMPLATE = """\
### {app_name}

{models}
"""

DICTIOANRY_RENDER_TEMPLATE = """\
# {project_name} - Data Dictionary

Commit `{commit}`

---

## Table of Contents [#](#toc)

{toc}

---

## Modules [#](#modules)

{apps}

"""


class DataDictionary:
    model_array_class = ModelArray

    @classmethod
    def get_data_dictionary(
        cls, apps: Optional[List[str]] = None
    ) -> Dict[str, ModelDefinition]:
        model_map = {}
        for model in ModelArray.get_models(valid_apps=apps, dialect=Dialect.MERMAID):
            name = (
                f"{(cls := model.django_model)._meta.app_label}.models.{cls.__name__}"
            )
            model_map[name] = model
        return model_map

    @classmethod
    def get_apps_map(
        cls, apps: Optional[List[str]] = None
    ) -> Dict[str, List[ModelDefinition]]:
        data_dictionary = cls.get_data_dictionary(apps=apps)
        apps_map = defaultdict(list)
        for model_name, model in data_dictionary.items():
            app_label = model.django_model._meta.app_label
            setattr(model, "name", model_name)
            apps_map[app_label].append(model)
        return apps_map

    @classmethod
    def render_model(cls, model: ModelDefinition) -> str:
        doc_string = model.django_model.__doc__ or "No description provided."
        doc_string = doc_string.strip()

        fields = []
        for field in model._fields:
            meta = field.django_field.__dict__
            related = meta.get("related_model")
            fields.append(
                {
                    "pk": "✓" if meta.get("primary_key") else "",
                    "field_name": field._col_name,
                    "data_type": f"`{field._data_type['data_type'].replace('_', ' ') or ''}`",
                    "related_model": f"[{related.__name__}](#{related.__name__})"
                    if related
                    else related.__name__
                    if related
                    else "",
                    "description": meta.get("help_text", "").replace("\n", " "),
                    "nullable": "✓" if meta.get("null") else "",
                    "unique": "✓" if meta.get("unique") else "",
                    "choices": "✓" if meta.get("choices") else "",
                    "max_length": meta.get("max_length") or "",
                    "db_index": "✓" if meta.get("db_index") else "",
                }
            )
        table = Table(fields)

        model_name = model.name.split(".")[-1]
        signature = f"{model_name}({', '.join([i.name for i in model.django_model._meta.get_fields() if i.concrete])})"
        model_name = f"{model_name}[#](#{model.django_model.__name__})"

        if doc_string[: len(model_name)] == signature[: len(model_name)]:
            doc_string = ""

        return MODEL_RENDER_TEMPLATE.format(
            model_name=model_name,
            doc_string=doc_string,
            signature=signature,
            table=table,
        )

    @classmethod
    def generate_data_dictionary(cls, apps: Optional[List[str]] = None) -> str:
        apps_map = cls.get_apps_map(apps=apps)

        rendered_apps: List[str] = []

        project_name = "Django Project"
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        if settings_module:
            project_name = settings_module.split(".")[0]

        toc = ["- [Table of Contents](#toc)", "- [Modules](#modules)"]
        for app, arr in apps_map.items():
            toc.append(f"  - [{app}](#{app})")

            apps_map[app] = sorted(arr, key=lambda x: x.django_model.__name__)

            rendered_models: List[str] = []
            for model in arr:
                model_name = model.django_model.__name__
                toc.append(f"    - [{model_name}](#{model_name})")
                rendered_models.append(cls.render_model(model))
            apps_map[app] = APPS_RENDER_TEMPLATE.format(
                app_name=app,
                models="\n".join(rendered_models),
            )
            rendered_apps.append(apps_map[app])

        return DICTIOANRY_RENDER_TEMPLATE.format(
            project_name=project_name,
            apps="\n".join(rendered_apps),
            commit=get_git_commit(),
            toc="\n".join(toc),
        ).replace("\n\n\n", "\n")

    @classmethod
    def save_data_dictionary(
        cls,
        path: str,
        apps: Optional[List[str]] = None,
    ) -> None:
        content = cls.generate_data_dictionary(apps=apps)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Data dictionary saved to {path}")

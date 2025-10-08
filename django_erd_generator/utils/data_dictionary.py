"""
Data dictionary generation utilities.

This module provides comprehensive functionality for generating Markdown-formatted
data dictionaries from Django models. It extracts model metadata, field information,
relationships, and constraints to create structured documentation suitable for
technical documentation, API docs, and team onboarding materials.

Key Features:
- Comprehensive field documentation with types, constraints, and relationships
- Table of contents with navigation links
- Git version tracking for documentation correlation
- Structured organization by Django app
- Markdown table formatting for consistent presentation
"""

from collections import defaultdict
import os
from typing import Dict, List, Optional
from django_erd_generator.contrib.dialects import Dialect
from django_erd_generator.contrib.markdown import Table
from django_erd_generator.definitions.models import ModelArray, ModelDefinition
from django_erd_generator.utils.git import get_git_commit

# Template for rendering individual model documentation
MODEL_RENDER_TEMPLATE = """\
#### {model_name}

`{signature}`

{doc_string}

{table}
"""

# Template for rendering app-level documentation sections
APPS_RENDER_TEMPLATE = """\
### {app_name}

{models}
"""

# Template for the complete data dictionary document
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
    """
    Main class for generating data dictionary documentation.

    This class provides static methods for extracting Django model information
    and generating comprehensive Markdown documentation. It handles model
    discovery, field analysis, relationship mapping, and document formatting
    with proper navigation and version tracking.

    The generated documentation includes:
    - Project-level header with git commit information
    - Table of contents with clickable navigation
    - App-organized model documentation
    - Detailed field tables with all metadata
    - Cross-references between related models

    Example:
        >>> # Generate for all apps
        >>> docs = DataDictionary.generate_data_dictionary()
        >>>
        >>> # Generate for specific apps
        >>> docs = DataDictionary.generate_data_dictionary(['myapp', 'core'])
        >>>
        >>> # Save to file
        >>> DataDictionary.save_data_dictionary(
        ...     apps=['myapp'],
        ...     path='docs/schema.md'
        ... )
    """

    model_array_class = ModelArray

    @classmethod
    def get_data_dictionary(
        cls, apps: Optional[List[str]] = None
    ) -> Dict[str, ModelDefinition]:
        """
        Extract and organize model definitions for data dictionary generation.

        Retrieves Django models from specified apps and creates a mapping
        of fully qualified model names to ModelDefinition objects.

        Args:
            apps: List of app labels to include, or None for all apps

        Returns:
            Dictionary mapping model names (app.models.ModelName) to ModelDefinition objects
        """
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
        """
        Organize models by Django app for structured documentation.

        Groups model definitions by their Django app labels to enable
        app-organized documentation generation.

        Args:
            apps: List of app labels to include, or None for all apps

        Returns:
            Dictionary mapping app labels to lists of ModelDefinition objects
        """
        data_dictionary = cls.get_data_dictionary(apps=apps)
        apps_map = defaultdict(list)
        for model_name, model in data_dictionary.items():
            app_label = model.django_model._meta.app_label
            setattr(model, "name", model_name)
            apps_map[app_label].append(model)
        return apps_map

    @classmethod
    def render_model(cls, model: ModelDefinition) -> str:
        """
        Generate Markdown documentation for a single Django model.

        Creates comprehensive documentation for a model including its signature,
        docstring, and a detailed field table with all metadata. Handles
        cross-references to related models and formats constraints appropriately.

        Args:
            model: ModelDefinition object to document

        Returns:
            Markdown string containing complete model documentation
        """
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
        """
        Generate complete data dictionary documentation in Markdown format.

        Creates a comprehensive data dictionary document including project header,
        table of contents, and detailed model documentation organized by app.
        Automatically detects project name and includes git commit information.

        Args:
            apps: List of app labels to include, or None for all apps

        Returns:
            Complete Markdown data dictionary document as a string
        """
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
        """
        Generate and save data dictionary documentation to a file.

        Convenience method that generates a complete data dictionary and
        saves it to the specified file path with UTF-8 encoding.

        Args:
            path: File path where the data dictionary should be saved
            apps: List of app labels to include, or None for all apps

        Example:
            >>> DataDictionary.save_data_dictionary(
            ...     path='docs/schema.md',
            ...     apps=['myapp', 'core']
            ... )
        """
        content = cls.generate_data_dictionary(apps=apps)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Data dictionary saved to {path}")

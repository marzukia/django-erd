# Django ERD Generator

![logo](https://github.com/marzukia/django-erd/blob/main/docs/img/logo.png?raw=true)

Django ERD Generator is a comprehensive command-line tool designed to generate Entity-Relationship Diagrams (ERDs) and data dictionaries from Django models. It supports multiple output formats, making it easy to visualise database relationships in different diagramming tools and create detailed documentation.

## Quick Overview

- **ERD Generation**: Create visual database diagrams in multiple formats
- **Data Dictionary**: Generate comprehensive model documentation in Markdown
- **Multiple Dialects**: Support for Mermaid.js, PlantUML, and dbdiagram.io
- **Flexible Output**: Console output or file export
- **App Filtering**: Include specific Django apps or all apps
- **Rich Documentation**: Field types, constraints, relationships, and help text

## Supported ERD Dialects

- Mermaid.js
- PlantUML
- dbdiagram.io

## Installation

```bash
pip install django-erd-generator
```

Add `'django_erd_generator'` to your `INSTALLED_APPS` in Django settings.

## Quick Start

Generate an ERD in Mermaid format:

```bash
python manage.py generate_erd -d mermaid
```

Generate a data dictionary:

```bash
python manage.py generate_data_dictionary -o docs/data_dictionary.md
```

## Why Use Django ERD Generator?

Keeping database schema documentation up to date is challenging. This tool automates the process by:

1. **Auto-generating diagrams** from your Django models
2. **Creating data dictionaries** with field details and relationships
3. **Supporting multiple formats** for different tools and platforms
4. **Staying in sync** with your codebase - just regenerate when models change

## Next Steps

- [Installation Guide](installation.md) - Detailed setup instructions
- [Quickstart Guide](quickstart.md) - Get started in 5 minutes
- [Features Overview](features/erd-generation.md) - Explore all capabilities

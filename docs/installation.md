# Installation

## Requirements

- Python 3.9+
- Django 4.2+

## Install via pip

```bash
pip install django-erd-generator
```

## Add to Django Project

Add `'django_erd_generator'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "django_erd_generator",
]
```

## Development Installation

For contributing or running tests:

```bash
# Clone the repository
git clone https://github.com/marzukia/django-erd.git
cd django-erd

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv sync --dev
```

## Verify Installation

Run the help command to verify installation:

```bash
python manage.py generate_erd --help
python manage.py generate_data_dictionary --help
```

## Optional: GIS Support

If you want to use GIS fields (PointField, PolygonField, etc.), make sure you have GeoDjango set up:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.gis",
    "django_erd_generator",
]
```

See [GIS Fields](features/gis-fields.md) for more details.

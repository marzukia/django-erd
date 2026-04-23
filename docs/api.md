# API Reference

Command-line interface reference for Django ERD Generator.

## generate_erd

Generate Entity-Relationship Diagram from Django models.

### Command

```bash
python manage.py generate_erd [options]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `-h, --help` | flag | - | Show help message |
| `-a, --apps` | string | All apps | Comma-separated list of apps to include |
| `-d, --dialect` | string | `mermaid` | Output format: `mermaid`, `plantuml`, `dbdiagram` |
| `-o, --output` | string | Console | Output file path |

### Examples

```bash
# Generate Mermaid ERD to console
python manage.py generate_erd -d mermaid

# Generate PlantUML ERD to file
python manage.py generate_erd -d plantuml -o erd.puml

# Generate ERD for specific apps
python manage.py generate_erd -a auth,shop -d dbdiagram
```

## generate_data_dictionary

Generate Markdown data dictionary from Django models.

### Command

```bash
python manage.py generate_data_dictionary [options]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `-h, --help` | flag | - | Show help message |
| `-a, --apps` | string | All apps | Comma-separated list of apps to include |
| `-o, --output` | string | Console | Output file path |

### Examples

```bash
# Generate data dictionary to console
python manage.py generate_data_dictionary

# Generate data dictionary to file
python manage.py generate_data_dictionary -o docs/data_dictionary.md

# Generate for specific apps only
python manage.py generate_data_dictionary -a shop -o docs/shop_dictionary.md
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (missing models, invalid options, etc.) |

## Errors

Common errors and solutions:

- **`Models not found`**: Check app names in `-a` parameter
- **`Dialect not supported`**: Use `mermaid`, `plantuml`, or `dbdiagram`
- **`Database not configured`**: Run `python manage.py migrate` first

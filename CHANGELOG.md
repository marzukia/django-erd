# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GIS field support for GeoDjango models (PointField, PolygonField, etc.)
- Support for multiple ERD dialects: Mermaid.js, PlantUML, dbdiagram.io
- Data dictionary generation in Markdown format

### Changed
- Migrated from black/flake8 to ruff for linting and formatting
- Dropped Python 3.8 support

### Fixed
- Typo in help text: "seperated" → "separated"
- Variable name typo: `DICTIOANRY_RENDER_TEMPLATE` → `DICTIONARY_RENDER_TEMPLATE`

## [0.1.0] - 2024-XX-XX

### Added
- Initial release
- ERD generation functionality
- Data dictionary generation
- Support for Mermaid.js, PlantUML, and dbdiagram.io dialects
- App filtering for selective model inclusion

# Contributing to Django ERD Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/django-erd.git
   cd django-erd
   ```
3. Set up the development environment:
   ```bash
   uv sync --dev
   ```

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they follow the project's coding standards:
   ```bash
   ruff check .
   ruff format .
   pytest
   ```

3. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "feat: add new feature"
   ```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update CHANGELOG.md with your changes under the [Unreleased] section
3. Ensure all tests pass
4. Submit a pull request with a clear description of your changes

## Code Style

- We use `ruff` for linting and formatting
- Follow PEP 8 style guidelines
- Write type hints for function signatures
- Add docstrings for public modules, classes, and functions

## Reporting Issues

- Use the GitHub issue tracker
- Provide a clear description of the issue
- Include steps to reproduce if it's a bug
- Attach relevant logs or screenshots

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

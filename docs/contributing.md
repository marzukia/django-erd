# Contributing

Thanks for your interest in contributing to Django ERD Generator!

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/django-erd.git
   cd django-erd
   ```

2. **Install dependencies**
   ```bash
   uv sync --dev
   ```

3. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make your changes

3. Run tests:
   ```bash
   pytest
   ```

4. Run linter and formatter:
   ```bash
   ruff check .
   ruff format .
   ```

5. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```

6. Push and create a pull request

## Code Style

- **Formatting**: ruff (line length: 88)
- **Linting**: ruff (E, F, W, I, UP, B, C4, SIM)
- **Type hints**: Preferred but not required

## Testing

- Write tests for new features
- Maintain test coverage
- Run `pytest` before submitting PR

## Pull Request Guidelines

1. Clear title and description
2. Link related issues
3. Update documentation if needed
4. Ensure all tests pass
5. Add changelog entry

## Questions?

Open an issue for questions or discussion.

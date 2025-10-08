#!/bin/sh
uv pip install build && uv run python -m build && TWINE_USERNAME=__token__ TWINE_PASSWORD=$PYPI_TOKEN uv run python -m twine upload dist/*
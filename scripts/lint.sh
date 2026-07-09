#!/usr/bin/env bash

set -e

echo "Running lint..."

uv run ruff check . --fix
uv run mypy app

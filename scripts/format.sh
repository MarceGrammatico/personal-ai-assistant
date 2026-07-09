#!/usr/bin/env bash

set -e

echo "Formatting code..."

uv run ruff format .
uv run ruff check . --fix

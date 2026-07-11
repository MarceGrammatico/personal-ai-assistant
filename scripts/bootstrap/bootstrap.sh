#!/usr/bin/env bash

set -e

PROJECT_NAME="personal-ai-assistant"

echo "🚀 Creating project structure: ${PROJECT_NAME}"

# Crear directorio raíz
mkdir -p "$PROJECT_NAME"

cd "$PROJECT_NAME"

echo "📁 Creating directories..."

# App structure
mkdir -p app/api/{routers,middleware,dependencies}
mkdir -p app/ai/{agents,chat,memory,prompts,tools}
mkdir -p app/core
mkdir -p app/plugins/{base,manager,registry}
mkdir -p app/services
mkdir -p app/shared
mkdir -p app/utils

# Config
mkdir -p config

# Docker
mkdir -p docker

# Documentation
mkdir -p docs/{adr,api,architecture,diagrams,roadmap}

# Scripts
mkdir -p scripts

# Tests
mkdir -p tests/{unit,integration,e2e}

# Github
mkdir -p .github/workflows

# VS Code
mkdir -p .devcontainer
mkdir -p .vscode


echo "📄 Creating files..."

# Python package init files
touch app/__init__.py

touch app/api/__init__.py
touch app/ai/__init__.py
touch app/core/__init__.py
touch app/plugins/__init__.py
touch app/services/__init__.py
touch app/shared/__init__.py
touch app/utils/__init__.py

# Core files
touch app/core/config.py
touch app/core/logging.py
touch app/core/constants.py

# Application entrypoint
touch app/main.py

# Root configuration files
touch Dockerfile
touch docker-compose.yml
touch pyproject.toml
touch .env.example
touch .editorconfig
touch .gitignore

# Documentation
touch README.md
touch ROADMAP.md
touch VISION.md
touch MANIFEST.md
touch CHANGELOG.md


echo "✅ Project bootstrap completed."

echo ""
echo "Structure created:"
tree -a -L 3

echo ""
echo "Next steps:"
echo "1. cd ${PROJECT_NAME}"
echo "2. git init"
echo "3. git checkout -b develop"
echo "4. git checkout -b feature/us-001-bootstrap"

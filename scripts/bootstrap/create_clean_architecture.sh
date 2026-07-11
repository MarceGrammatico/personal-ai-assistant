#!/usr/bin/env bash

set -euo pipefail

echo "📦 Creating Clean Architecture directories..."

# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------

mkdir -p app/application/{dto,interfaces,services,commands,queries}

touch \
    app/application/__init__.py \
    app/application/dto/__init__.py \
    app/application/interfaces/__init__.py \
    app/application/services/__init__.py \
    app/application/commands/__init__.py \
    app/application/queries/__init__.py

# -----------------------------------------------------------------------------
# Domain
# -----------------------------------------------------------------------------

mkdir -p app/domain/{agents,chat,memory,plugins,tools,models}

touch \
    app/domain/__init__.py \
    app/domain/agents/__init__.py \
    app/domain/chat/__init__.py \
    app/domain/memory/__init__.py \
    app/domain/plugins/__init__.py \
    app/domain/tools/__init__.py \
    app/domain/models/__init__.py

# -----------------------------------------------------------------------------
# Infrastructure
# -----------------------------------------------------------------------------

mkdir -p app/infrastructure/{llm,jira,github,persistence,vectorstore,cache}

touch \
    app/infrastructure/__init__.py \
    app/infrastructure/llm/__init__.py \
    app/infrastructure/jira/__init__.py \
    app/infrastructure/github/__init__.py \
    app/infrastructure/persistence/__init__.py \
    app/infrastructure/vectorstore/__init__.py \
    app/infrastructure/cache/__init__.py

echo "✅ Clean Architecture structure created successfully."

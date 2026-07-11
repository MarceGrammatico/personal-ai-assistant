#!/usr/bin/env bash

set -euo pipefail

echo "🧪 Creating test structure..."

# ==============================================================================
# Directories
# ==============================================================================

mkdir -p \
    tests/integration \
    tests/unit/api/middleware \
    tests/unit/api/routers \
    tests/unit/application/commands \
    tests/unit/application/queries \
    tests/unit/application/services \
    tests/unit/domain \
    tests/unit/infrastructure/github \
    tests/unit/infrastructure/jira \
    tests/unit/infrastructure/llm \
    tests/unit/infrastructure/persistence \
    tests/unit/infrastructure/vectorstore \
    tests/unit/shared

# ==============================================================================
# __init__.py
# ==============================================================================

touch \
    tests/__init__.py \
    tests/integration/__init__.py \
    tests/unit/__init__.py \
    tests/unit/api/__init__.py \
    tests/unit/api/middleware/__init__.py \
    tests/unit/api/routers/__init__.py \
    tests/unit/application/__init__.py \
    tests/unit/application/commands/__init__.py \
    tests/unit/application/queries/__init__.py \
    tests/unit/application/services/__init__.py \
    tests/unit/domain/__init__.py \
    tests/unit/infrastructure/__init__.py \
    tests/unit/infrastructure/github/__init__.py \
    tests/unit/infrastructure/jira/__init__.py \
    tests/unit/infrastructure/llm/__init__.py \
    tests/unit/infrastructure/persistence/__init__.py \
    tests/unit/infrastructure/vectorstore/__init__.py \
    tests/unit/shared/__init__.py

# ==============================================================================
# Domain tests
# ==============================================================================

touch \
    tests/unit/domain/test_message.py \
    tests/unit/domain/test_conversation.py \
    tests/unit/domain/test_prompt.py \
    tests/unit/domain/test_tool.py \
    tests/unit/domain/test_tool_call.py \
    tests/unit/domain/test_chat_request.py \
    tests/unit/domain/test_chat_response.py

# ==============================================================================
# Application tests
# ==============================================================================

touch \
    tests/unit/application/commands/.gitkeep \
    tests/unit/application/queries/.gitkeep \
    tests/unit/application/services/.gitkeep

# ==============================================================================
# Infrastructure tests
# ==============================================================================

touch \
    tests/unit/infrastructure/llm/.gitkeep \
    tests/unit/infrastructure/github/.gitkeep \
    tests/unit/infrastructure/jira/.gitkeep \
    tests/unit/infrastructure/persistence/.gitkeep \
    tests/unit/infrastructure/vectorstore/.gitkeep

# ==============================================================================
# API tests
# ==============================================================================

touch \
    tests/unit/api/middleware/.gitkeep \
    tests/unit/api/routers/.gitkeep

# ==============================================================================
# Shared tests
# ==============================================================================

touch \
    tests/unit/shared/.gitkeep

echo
echo "=============================================="
echo "✅ Test structure created successfully!"
echo "=============================================="

echo
echo "Created:"
echo "  • tests/integration"
echo "  • tests/unit/api"
echo "  • tests/unit/application"
echo "  • tests/unit/domain"
echo "  • tests/unit/infrastructure"
echo "  • tests/unit/shared"
echo

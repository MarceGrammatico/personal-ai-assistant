# 🤖 Personal AI Assistant

A modular, multi-provider AI assistant platform with web interface, CLI, Jira integration, and web search capabilities. Built with Clean Architecture principles for scalability, testability, and maintainability.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [LLM Providers](#llm-providers)
- [Integrations](#integrations)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Docker](#docker)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

---

## Features

- **Multi-provider LLM support** — OpenAI, Ollama (local models), or Fake (testing)
- **Real-time streaming** — Server-Sent Events (SSE) for live response generation
- **Conversation persistence** — SQLite storage with full message history
- **Web search** — DuckDuckGo integration via function calling
- **Jira integration** — Query, create, and manage issues via natural language
- **Web frontend** — Chat UI with conversation sidebar, settings panel
- **Terminal CLI** — Colorized streaming chat client
- **Runtime configuration** — Change provider, model, temperature without restart
- **Tool calling** — Extensible tool system for adding new capabilities
- **Clean Architecture** — Domain-driven, testable, provider-agnostic design

---

## Architecture

The project follows **Clean Architecture** (Hexagonal/Ports & Adapters):

```
┌─────────────────────────────────────────────────┐
│                   API Layer                       │
│         (Routers, Middleware, Handlers)           │
├─────────────────────────────────────────────────┤
│              Application Layer                    │
│    (Use Cases, Services, Commands, DTOs, Tools)  │
├─────────────────────────────────────────────────┤
│                Domain Layer                       │
│       (Entities, Value Objects, Enums)           │
├─────────────────────────────────────────────────┤
│             Infrastructure Layer                  │
│   (LLM Providers, Persistence, Jira Client)      │
└─────────────────────────────────────────────────┘
```

**Dependency rule**: Dependencies always point inward. Infrastructure implements interfaces defined in the Application layer.

---

## Project Structure

```
personal-ai-assistant/
├── app/
│   ├── main.py                          # Application entry point
│   ├── factory.py                       # FastAPI app factory
│   ├── api/
│   │   ├── handlers/                    # Exception handlers
│   │   ├── middleware/                  # Request context (request ID)
│   │   └── routers/                     # API endpoints
│   │       ├── chat.py                  # POST /chat, GET/DELETE conversations
│   │       ├── health.py               # GET /health
│   │       ├── settings.py             # GET/PUT /settings
│   │       ├── system.py               # GET /info
│   │       └── root.py                 # GET /
│   ├── application/
│   │   ├── commands/                    # ChatCommand (builds requests)
│   │   ├── dependencies.py             # Dependency injection
│   │   ├── dto/                         # Data Transfer Objects
│   │   ├── exceptions/                  # Application exceptions
│   │   ├── interfaces/                  # Ports (contracts)
│   │   │   ├── llm_provider.py         # LLM provider interface
│   │   │   ├── conversation_repository.py
│   │   │   └── jira_client.py
│   │   ├── services/                    # ChatService (orchestration)
│   │   ├── tools/                       # Function calling tools
│   │   │   ├── registry.py             # Tool registry
│   │   │   ├── web_tools.py            # Web search & fetch
│   │   │   └── jira_tools.py           # Jira operations
│   │   └── use_cases/                   # SendMessageUseCase
│   ├── core/
│   │   ├── config.py                    # Settings (pydantic-settings)
│   │   ├── enums.py                     # Environment, Provider, Storage enums
│   │   ├── exceptions.py               # Base exception hierarchy
│   │   ├── error_codes.py              # Error code constants
│   │   ├── logging.py                  # Logging configuration
│   │   └── context.py                  # Request ID context var
│   ├── domain/
│   │   └── models/                      # Domain models
│   │       ├── conversation.py          # Conversation entity
│   │       ├── message.py              # Message value object
│   │       ├── chat_request.py         # LLM request model
│   │       ├── chat_response.py        # LLM response model
│   │       ├── usage.py                # Token usage model
│   │       ├── entity.py               # Base entity (mutable)
│   │       └── value_object.py         # Base value object (immutable)
│   ├── infrastructure/
│   │   ├── jira/                        # Jira Cloud REST API client
│   │   ├── llm/
│   │   │   ├── fake/                   # Fake provider (testing)
│   │   │   ├── openai/                 # OpenAI provider
│   │   │   └── ollama/                 # Ollama provider (local)
│   │   └── persistence/
│   │       ├── in_memory_conversation_repository.py
│   │       └── sqlite_conversation_repository.py
│   └── schemas/                         # Pydantic response schemas
├── frontend/
│   └── index.html                       # Chat web interface
├── cli/
│   └── __main__.py                      # Terminal chat client
├── tests/
│   ├── conftest.py                      # Shared fixtures
│   ├── integration/                     # API integration tests
│   └── unit/                            # Unit tests by layer
├── data/                                # SQLite database (gitignored)
├── Modelfile                            # Ollama custom model definition
├── Dockerfile                           # Container image
├── docker-compose.yml                   # Docker Compose config
├── pyproject.toml                       # Project config & dependencies
├── Makefile                             # Development commands
└── .env.example                         # Environment variables template
```

---

## Requirements

- **Python** 3.13+
- **uv** (package manager) — https://docs.astral.sh/uv/
- **Ollama** (optional, for local models) — https://ollama.ai
- **Docker** (optional) — for containerized deployment

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd personal-ai-assistant

# Install dependencies
uv sync

# Copy environment configuration
cp .env.example .env

# Edit .env with your settings
nano .env
```

---

## Configuration

All configuration is done via environment variables (`.env` file):

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Personal AI Assistant | Application name |
| `APP_VERSION` | 0.1.0 | Application version |
| `DEBUG` | true | Debug mode |
| `ENVIRONMENT` | development | Environment (development/test/production) |
| `LOG_LEVEL` | INFO | Log level (DEBUG/INFO/WARNING/ERROR) |

### LLM Provider

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | fake | Provider: `fake`, `openai`, or `ollama` |
| `OPENAI_API_KEY` | | OpenAI API key |
| `OPENAI_MODEL` | gpt-4o-mini | OpenAI model name |
| `OPENAI_TIMEOUT` | 60 | OpenAI request timeout (seconds) |
| `OLLAMA_BASE_URL` | http://localhost:11434 | Ollama server URL |
| `OLLAMA_MODEL` | llama3.1:8b | Ollama model name |

### System Prompt

| Variable | Default | Description |
|----------|---------|-------------|
| `SYSTEM_PROMPT` | (see .env.example) | Assistant personality and instructions |

### Storage

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_TYPE` | sqlite | Storage backend: `memory` or `sqlite` |
| `SQLITE_DB_PATH` | data/conversations.db | SQLite database path |

### Conversation

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_CONVERSATION_TOKENS` | 4096 | Max tokens in history (OpenAI only) |
| `MAX_CONVERSATION_MESSAGES` | 50 | Max messages in history (OpenAI only) |

### Jira Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `JIRA_ENABLED` | false | Enable Jira integration |
| `JIRA_DOMAIN` | | Jira Cloud domain (e.g., `your-org.atlassian.net`) |
| `JIRA_EMAIL` | | Jira account email |
| `JIRA_API_TOKEN` | | Jira API token |

---

## Usage

### Start the Server

```bash
# Local development (with hot reload)
make run

# Or directly
uv run uvicorn app.main:app --reload --port 8000
```

### Web Frontend

Open **http://localhost:8000/app** in your browser.

Features:
- Real-time streaming responses
- Conversation history sidebar
- Click to load previous conversations
- Delete conversations
- Settings panel (⚙️) for runtime configuration

### Terminal CLI

```bash
# Start the CLI chat
make chat

# Or directly
uv run python -m cli

# Options
uv run python -m cli --no-stream      # Disable streaming
uv run python -m cli --base-url http://other-host:8000
```

CLI commands:
- `exit` — Quit
- `new` — Start a new conversation
- `Ctrl+C` — Quit

### API (Swagger)

Open **http://localhost:8000/docs** for interactive API documentation.

---

## LLM Providers

### Fake (Testing)

Always returns a fixed response. Useful for development and testing.

```env
LLM_PROVIDER=fake
```

### OpenAI

Requires an API key with billing enabled.

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

Supports: streaming, function calling (web search, Jira).

### Ollama (Local Models)

Run models locally with no restrictions, no costs, no data sent externally.

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Download a model
ollama pull huihui_ai/qwen3-abliterated
```

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=huihui_ai/qwen3-abliterated:latest
```

#### Recommended Local Models

| Model | Command | Tools | Uncensored | Notes |
|-------|---------|-------|------------|-------|
| Qwen3 Abliterated | `ollama pull huihui_ai/qwen3-abliterated` | ✅ | ✅ | Best all-around |
| Dolphin3 Abliterated | `ollama pull huihui_ai/dolphin3-abliterated` | ✅ | ✅ | Good alternative |
| DeepSeek R1 Abliterated | `ollama pull huihui_ai/deepseek-r1-abliterated` | ❌ | ✅ | Best reasoning |
| LLaMA 3.1 8B | `ollama pull llama3.1:8b` | ✅ | ❌ | Meta's official |

#### Custom Model (Modelfile)

Create a `Modelfile` to customize personality:

```dockerfile
FROM huihui_ai/qwen3-abliterated:latest

SYSTEM """
Your custom system prompt here.
"""

PARAMETER temperature 0.8
PARAMETER num_ctx 8192
```

```bash
ollama create my-assistant -f Modelfile
```

Then set `OLLAMA_MODEL=my-assistant` in `.env`.

---

## Integrations

### Web Search

Enabled by default for providers that support tools (OpenAI, Ollama with tool-capable models). Uses DuckDuckGo — no API key needed.

The assistant can:
- Search the web for current information
- Fetch and read specific URLs

### Jira

1. Generate an API token at https://id.atlassian.com/manage-profile/security/api-tokens
2. Configure `.env`:

```env
JIRA_ENABLED=true
JIRA_DOMAIN=your-org.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token
```

The assistant can:
- List your assigned issues
- Get issue details
- Search with JQL
- Create issues
- Add comments
- Transition issue status

### Google Calendar

Allows the assistant to read, create, search, and delete events from your Google Calendar.

#### Setup

**1. Create a Google Cloud Project**

1. Go to https://console.cloud.google.com/
2. Create a new project (or select an existing one)
3. Enable the **Google Calendar API**: https://console.cloud.google.com/apis/library/calendar-json.googleapis.com

**2. Create OAuth2 Credentials**

1. Go to **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
2. Application type: **Desktop app**
3. Give it any name (e.g., "Personal AI Assistant")
4. Download the JSON file
5. Save it as `config/google_credentials.json` in the project root

**3. Configure OAuth Consent Screen** (first time only)

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** → Create
3. Fill in app name and your email
4. In **Scopes**, add `https://www.googleapis.com/auth/calendar`
5. In **Test users**, add your Gmail address
6. Save

**4. Authenticate** (one-time, opens browser)

```bash
make setup-calendar
```

This opens your browser, you authorize access, and the token is saved to `data/google_token.json`. You only need to do this once.

**5. Enable in `.env`**

```env
GOOGLE_CALENDAR_ENABLED=true
GOOGLE_CALENDAR_CREDENTIALS_PATH=config/google_credentials.json
GOOGLE_CALENDAR_TOKEN_PATH=data/google_token.json
```

**6. Restart the server**

```bash
make run
```

#### Usage

Start a **new conversation** and ask:
- "¿Qué tengo en el calendario hoy?"
- "Listame los eventos de esta semana"
- "Agendame una reunión mañana a las 15:00 llamada Standup"
- "Buscá en mi calendario reuniones con Pedro"
- "Eliminá el evento con ID xyz"

#### Requirements

- The LLM provider must support **tool calling** (OpenAI, or Ollama with a tool-capable model like `huihui_ai/qwen3-abliterated`)
- Models without tool support (e.g., `dolphin-mistral`, `deepseek-r1-abliterated`) cannot use calendar features

#### Troubleshooting

- **"Google Calendar is not configured"** → Ensure `GOOGLE_CALENDAR_ENABLED=true` in `.env`
- **Token expired** → Run `make setup-calendar` again
- **Model doesn't use the calendar tool** → Ensure you're using a tool-capable model and start a new conversation
- **First request is slow** → Normal with local models; the tool-calling loop requires multiple inferences

---

## API Reference

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send a message |
| GET | `/chat/conversations` | List all conversations |
| GET | `/chat/conversations/{id}` | Get conversation with messages |
| DELETE | `/chat/conversations/{id}` | Delete a conversation |

#### POST /chat

```json
{
  "message": "Hello",
  "conversation_id": "uuid (optional, to continue)",
  "stream": true
}
```

**Non-streaming response:**
```json
{
  "answer": "Hi! How can I help?",
  "conversation_id": "uuid",
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 10,
    "total_tokens": 60
  }
}
```

**Streaming response (SSE):**
```
data: {"type": "content", "data": "Hi"}
data: {"type": "content", "data": "! How"}
data: {"type": "content", "data": " can I help?"}
data: {"type": "done", "conversation_id": "uuid"}
```

### Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/settings` | Get current settings |
| PUT | `/settings` | Update settings at runtime |
| GET | `/settings/available-models` | List available providers & models |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/info` | System information |
| GET | `/` | Basic status |

---

## Development

### Commands

```bash
make help          # Show all commands
make run           # Start dev server (hot reload)
make chat          # Start terminal client
make test          # Run tests
make lint          # Run linter (ruff + mypy)
make format        # Format code
make clean         # Remove caches
```

### Adding a New LLM Provider

1. Create `app/infrastructure/llm/your_provider/`
2. Implement `LLMProvider` interface (`chat()` + `chat_stream()`)
3. Add to `LLMProviderType` enum in `app/core/enums.py`
4. Add to `get_llm_provider()` in `app/application/dependencies.py`
5. Provider automatically appears in frontend settings

### Adding a New Tool

1. Create tool definitions in `app/application/tools/your_tools.py`
2. Add to `ToolRegistry` in `app/application/tools/registry.py`
3. Add execution logic to `_execute_tool()` in providers

### Adding a New Storage Backend

1. Implement `ConversationRepository` interface
2. Add to `StorageType` enum in `app/core/enums.py`
3. Add to `get_conversation_repository()` in `app/application/dependencies.py`

---

## Testing

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/domain/test_conversation.py

# Run only integration tests
uv run pytest tests/integration/

# Run only unit tests
uv run pytest tests/unit/
```

Tests automatically use:
- `LLM_PROVIDER=fake` (no real API calls)
- `STORAGE_TYPE=memory` (no disk writes)

---

## Docker

```bash
# Build and start
docker compose up --build

# Run in background
docker compose up --build -d

# View logs
docker compose logs -f

# Stop
docker compose down

# Run tests in container
make docker-test

# Run linter in container
make docker-lint
```

The container:
- Uses Python 3.13
- Exposes port 8000
- Mounts source code for hot reload
- Protects container's `.venv` from host mount conflicts

---

## Contributing

### Workflow

1. Create a feature branch from `develop`
2. Implement changes with tests
3. Ensure `make lint` and `make test` pass
4. Submit a pull request

### Code Style

- **Formatter**: Ruff (line length: 100)
- **Linter**: Ruff (rules: E, F, I, UP, B)
- **Type checking**: MyPy (strict mode)
- **Pre-commit**: Ruff format + check on every commit

### Commit Messages

Use conventional commits:

```
feat: add Ollama provider support
fix: resolve timeout in streaming responses
refactor: extract tool execution to separate method
test: add SQLite repository persistence tests
docs: update README with Jira configuration
```

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include tests for new functionality
- Update documentation if adding user-facing features
- Ensure CI passes before requesting review

---

## Code of Conduct

### Our Standards

We are committed to providing a welcoming and inclusive environment. All participants are expected to:

- **Be respectful** — Treat everyone with dignity regardless of background, identity, or experience level
- **Be constructive** — Provide helpful feedback, accept criticism gracefully
- **Be collaborative** — Work together towards shared goals
- **Be professional** — Keep discussions technical and on-topic

### Unacceptable Behavior

- Harassment, discrimination, or intimidation of any kind
- Personal attacks or derogatory comments
- Publishing others' private information without permission
- Any conduct that would be inappropriate in a professional setting

### Scope

This code of conduct applies to all project spaces including issues, pull requests, discussions, and any related communication channels.

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

Copyright 2026 Marcelo Grammaticopiraino

---

## Troubleshooting

### Common Issues

**"An error occurred while generating the response"**
- Check the terminal where `make run` is running for the actual error
- If using Ollama: ensure `ollama serve` is running
- If using OpenAI: verify your API key has billing enabled

**Ollama timeout errors**
- Normal for first request after inactivity (model loading)
- Keep Ollama running: `OLLAMA_KEEP_ALIVE=30m ollama serve`
- The app has no timeout limit for local models

**Jira 410 Gone errors**
- The project uses the new `/rest/api/3/search/jql` endpoint
- Ensure your Jira instance is Cloud (not Server/Data Center)

**Frontend not updating after changes**
- Hard refresh: `Ctrl+Shift+R`
- Start a new conversation for system prompt changes to take effect

**Docker `.venv` conflicts**
- Run `docker compose down` before running locally
- The docker-compose uses an anonymous volume to protect the container's venv

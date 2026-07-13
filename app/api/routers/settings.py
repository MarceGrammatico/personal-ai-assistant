import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings
from app.core.enums import LLMProviderType

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


class SettingsDTO(BaseModel):
    """Exposed settings that can be viewed/modified at runtime."""

    llm_provider: str
    openai_model: str
    ollama_model: str
    ollama_base_url: str
    temperature: float
    max_conversation_messages: int
    system_prompt: str


class UpdateSettingsDTO(BaseModel):
    """Fields that can be updated at runtime."""

    llm_provider: str | None = None
    openai_model: str | None = None
    ollama_model: str | None = None
    ollama_base_url: str | None = None
    temperature: float | None = None
    max_conversation_messages: int | None = None
    system_prompt: str | None = None


# Runtime temperature (not in Settings model, managed here)
_runtime_temperature: float = 0.7


def get_temperature() -> float:
    return _runtime_temperature


@router.get("", response_model=SettingsDTO)
async def get_settings() -> SettingsDTO:
    """Get current assistant settings."""

    return SettingsDTO(
        llm_provider=settings.LLM_PROVIDER.value,
        openai_model=settings.OPENAI_MODEL,
        ollama_model=settings.OLLAMA_MODEL,
        ollama_base_url=settings.OLLAMA_BASE_URL,
        temperature=_runtime_temperature,
        max_conversation_messages=settings.MAX_CONVERSATION_MESSAGES,
        system_prompt=settings.SYSTEM_PROMPT,
    )


@router.put("", response_model=SettingsDTO)
async def update_settings(update: UpdateSettingsDTO) -> SettingsDTO:
    """
    Update assistant settings at runtime.
    Changes are temporary (reset on server restart).
    """

    global _runtime_temperature

    if update.llm_provider is not None:
        settings.LLM_PROVIDER = LLMProviderType(update.llm_provider)

    if update.openai_model is not None:
        settings.OPENAI_MODEL = update.openai_model

    if update.ollama_model is not None:
        settings.OLLAMA_MODEL = update.ollama_model

    if update.ollama_base_url is not None:
        settings.OLLAMA_BASE_URL = update.ollama_base_url

    if update.temperature is not None:
        _runtime_temperature = update.temperature

    if update.max_conversation_messages is not None:
        settings.MAX_CONVERSATION_MESSAGES = update.max_conversation_messages

    if update.system_prompt is not None:
        settings.SYSTEM_PROMPT = update.system_prompt

    return await get_settings()


@router.get("/available-models")
async def get_available_models() -> dict:
    """
    Get available providers and models dynamically.

    - Providers: detected from LLMProviderType enum (auto-updates when new ones are added)
    - OpenAI models: fetched from OpenAI API (requires valid API key)
    - Ollama models: fetched from local Ollama instance
    """

    providers = [p.value for p in LLMProviderType]

    ollama_models = await _fetch_ollama_models()
    openai_models = await _fetch_openai_models()

    return {
        "providers": providers,
        "openai_models": openai_models,
        "ollama_models": ollama_models,
    }


async def _fetch_ollama_models() -> list[str]:
    """Fetch available models from local Ollama instance."""

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
    except Exception:
        pass

    return []


async def _fetch_openai_models() -> list[str]:
    """
    Fetch available models from OpenAI API.
    Filters to chat-capable models only.
    """

    if not settings.OPENAI_API_KEY:
        return []

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.openai.com/v1/models",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                },
            )

            if resp.status_code != 200:
                return []

            data = resp.json()
            models = data.get("data", [])

            # Filter to GPT chat models (exclude embeddings, whisper, etc.)
            chat_models = sorted(
                m["id"]
                for m in models
                if any(prefix in m["id"] for prefix in ("gpt-", "o1", "o3", "chatgpt"))
                and "realtime" not in m["id"]
                and "audio" not in m["id"]
            )

            return chat_models

    except Exception:
        return []

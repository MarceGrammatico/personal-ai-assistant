import json
from collections.abc import AsyncIterator

import httpx

from app.core.config import settings


class OllamaClient:
    """
    Low-level Ollama API client.

    Ollama exposes an OpenAI-compatible API at /v1/chat/completions
    and also its native API at /api/chat.
    We use the native API for better streaming and tool support.
    """

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.OLLAMA_BASE_URL
        self._supports_tools: bool | None = None

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=120,
        )

    async def supports_tools(self) -> bool:
        """Check if the current model supports tool calling."""

        if self._supports_tools is not None:
            return self._supports_tools

        try:
            async with self._client() as client:
                resp = await client.post(
                    "/api/show",
                    json={"model": settings.OLLAMA_MODEL},
                )
                resp.raise_for_status()
                data = resp.json()
                capabilities = data.get("model_info", {}).get("capabilities", [])
                # Also check top-level details
                if not capabilities:
                    capabilities = data.get("details", {}).get("capabilities", [])
                self._supports_tools = "tools" in capabilities
        except Exception:
            self._supports_tools = False

        return self._supports_tools

    async def chat(
        self,
        *,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        """
        Send a chat completion request (non-streaming).
        """

        payload: dict = {
            "model": model,
            "messages": messages,
            "stream": False,
        }

        if tools and await self.supports_tools():
            payload["tools"] = tools

        async with self._client() as client:
            resp = await client.post("/api/chat", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def chat_stream(
        self,
        *,
        model: str,
        messages: list[dict],
    ) -> AsyncIterator[str]:
        """
        Send a streaming chat request.
        Yields content chunks as they arrive.
        """

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
        }

        async with self._client() as client:
            async with client.stream("POST", "/api/chat", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    content = data.get("message", {}).get("content", "")
                    if content:
                        yield content

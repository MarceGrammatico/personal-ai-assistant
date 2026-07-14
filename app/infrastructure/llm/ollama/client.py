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
        self._supports_tools_cache: dict[str, bool] = {}

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=None,
        )

    async def supports_tools(self) -> bool:
        """Check if the current model supports tool calling."""

        model = settings.OLLAMA_MODEL

        if model in self._supports_tools_cache:
            return self._supports_tools_cache[model]

        try:
            async with self._client() as client:
                resp = await client.post(
                    "/api/show",
                    json={"model": model},
                )
                resp.raise_for_status()
                data = resp.json()
                # capabilities can be at top-level, model_info, or details
                capabilities = data.get("capabilities", [])
                if not capabilities:
                    capabilities = data.get("model_info", {}).get("capabilities", [])
                if not capabilities:
                    capabilities = data.get("details", {}).get("capabilities", [])
                result = "tools" in capabilities
        except Exception:
            result = False

        self._supports_tools_cache[model] = result
        return result

    async def chat(
        self,
        *,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        temperature: float | None = None,
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

        options: dict = {"num_predict": -1}
        if temperature is not None:
            options["temperature"] = temperature
        payload["options"] = options

        async with self._client() as client:
            resp = await client.post("/api/chat", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def chat_stream(
        self,
        *,
        model: str,
        messages: list[dict],
        temperature: float | None = None,
    ) -> AsyncIterator[str]:
        """
        Send a streaming chat request.
        Yields content chunks as they arrive.
        """

        payload: dict = {
            "model": model,
            "messages": messages,
            "stream": True,
        }

        options: dict = {"num_predict": -1}
        if temperature is not None:
            options["temperature"] = temperature
        payload["options"] = options

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

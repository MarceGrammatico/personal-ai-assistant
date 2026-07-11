from collections.abc import AsyncIterator

from openai import APIError, APITimeoutError, AsyncOpenAI
from openai.types.chat import ChatCompletion

from app.core.config import settings
from app.infrastructure.llm.openai.exceptions import (
    OpenAIRequestError,
    OpenAITimeoutError,
)


class OpenAIClient:
    """
    Low-level OpenAI API client.
    """

    def __init__(
        self,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self._client = client or AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_TIMEOUT,
        )

    async def chat(
        self,
        *,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> ChatCompletion:
        """
        Send a chat completion request (non-streaming).
        Optionally includes tools for function calling.
        """

        kwargs: dict = {
            "model": model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools

        try:
            return await self._client.chat.completions.create(**kwargs)

        except APITimeoutError as exc:
            raise OpenAITimeoutError("OpenAI request timed out") from exc

        except APIError as exc:
            raise OpenAIRequestError("OpenAI request failed") from exc

    async def chat_stream(
        self,
        *,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """
        Send a streaming chat completion request.
        Yields content delta strings as they arrive.

        Note: streaming with function calling is not supported;
        if tools are provided and the model calls a tool, use
        non-streaming chat() instead.
        """

        kwargs: dict = {
            "model": model,
            "messages": messages,
            "stream": True,
        }

        # Don't pass tools in streaming mode — handle tool calls in non-streaming
        # The provider layer handles the tool-call loop before streaming the final answer

        try:
            stream = await self._client.chat.completions.create(**kwargs)

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except APITimeoutError as exc:
            raise OpenAITimeoutError("OpenAI request timed out") from exc

        except APIError as exc:
            raise OpenAIRequestError("OpenAI request failed") from exc

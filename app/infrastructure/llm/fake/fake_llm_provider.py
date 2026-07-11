import asyncio
from collections.abc import AsyncIterator

from app.application.interfaces.llm_provider import LLMProvider
from app.domain.models import (
    ChatRequest,
    ChatResponse,
    Message,
    MessageRole,
    Usage,
)

FAKE_RESPONSE = "Hello! I am a fake assistant."


class FakeLLMProvider(LLMProvider):
    """
    Fake implementation used for development and tests.
    """

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        return ChatResponse(
            message=Message(
                role=MessageRole.ASSISTANT,
                content=FAKE_RESPONSE,
            ),
            usage=Usage(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
            ),
        )

    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """
        Simulates streaming by yielding words with a small delay.
        """

        words = FAKE_RESPONSE.split(" ")

        for i, word in enumerate(words):
            await asyncio.sleep(0.05)
            yield word if i == 0 else f" {word}"

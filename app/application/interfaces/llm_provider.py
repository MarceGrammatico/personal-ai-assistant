from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.domain.models import ChatRequest, ChatResponse


class LLMProvider(ABC):
    """
    Contract implemented by every Large Language Model provider.
    """

    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Sends a chat request to an LLM and returns the complete response.
        """

    @abstractmethod
    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """
        Sends a chat request and yields response content chunks as they arrive.
        """

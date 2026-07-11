from collections.abc import AsyncIterator
from uuid import UUID

from app.application.services import ChatService
from app.domain.models import ChatResponse, Conversation


class SendMessageResult:
    """Result of sending a message."""

    def __init__(
        self,
        response: ChatResponse,
        conversation: Conversation,
    ) -> None:
        self.response = response
        self.conversation = conversation


class SendMessageUseCase:
    """
    Sends a user message and returns the assistant's response.
    Manages conversation context (new or existing).
    """

    def __init__(
        self,
        chat_service: ChatService,
    ) -> None:
        self._chat_service = chat_service

    async def execute(
        self,
        message: str,
        conversation_id: UUID | None = None,
    ) -> SendMessageResult:
        """
        Execute the use case (non-streaming).

        Returns a result containing the response and conversation.
        """

        response, conversation = await self._chat_service.chat(
            message=message,
            conversation_id=conversation_id,
        )

        return SendMessageResult(
            response=response,
            conversation=conversation,
        )

    async def execute_stream(
        self,
        message: str,
        conversation_id: UUID | None = None,
    ) -> tuple[Conversation, AsyncIterator[str]]:
        """
        Execute the use case in streaming mode.

        Returns the conversation and a content chunk iterator.
        """

        return await self._chat_service.chat_stream(
            message=message,
            conversation_id=conversation_id,
        )

    async def save_streamed_response(
        self,
        conversation: Conversation,
        content: str,
    ) -> None:
        """
        Persist the assistant's message after streaming completes.
        """

        await self._chat_service.save_assistant_message(
            conversation=conversation,
            content=content,
        )

from collections.abc import AsyncIterator
from uuid import UUID

from app.application.commands import ChatCommand
from app.application.interfaces.conversation_repository import ConversationRepository
from app.application.interfaces.llm_provider import LLMProvider
from app.domain.models import (
    ChatResponse,
    Conversation,
)


class ChatService:
    """
    Application service responsible for managing conversations
    and communicating with the configured LLM provider.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        conversation_repository: ConversationRepository,
        command: ChatCommand | None = None,
    ) -> None:
        self._llm_provider = llm_provider
        self._repository = conversation_repository
        self._command = command or ChatCommand()

    async def chat(
        self,
        message: str,
        conversation_id: UUID | None = None,
    ) -> tuple[ChatResponse, Conversation]:
        """
        Sends a message and returns the complete response.

        Maintains conversation history by persisting messages.
        Returns (response, conversation).
        """

        conversation = await self._get_or_create_conversation(
            conversation_id,
        )

        # Set title from first user message
        if conversation.is_empty():
            conversation.rename(self._generate_title(message))

        request = self._command.create_request(
            message=message,
            conversation=conversation,
        )

        response = await self._llm_provider.chat(request)

        conversation.add_message_from_assistant(
            response.message.content,
        )

        await self._repository.save(conversation)

        return response, conversation

    async def chat_stream(
        self,
        message: str,
        conversation_id: UUID | None = None,
    ) -> tuple[Conversation, AsyncIterator[str]]:
        """
        Sends a message and returns a streaming response.

        Returns the conversation and an async iterator of content chunks.
        The caller is responsible for collecting chunks and saving the
        assistant message after streaming completes.
        """

        conversation = await self._get_or_create_conversation(
            conversation_id,
        )

        # Set title from first user message
        if conversation.is_empty():
            conversation.rename(self._generate_title(message))

        request = self._command.create_request(
            message=message,
            conversation=conversation,
        )

        stream = self._llm_provider.chat_stream(request)

        return conversation, stream

    async def save_assistant_message(
        self,
        conversation: Conversation,
        content: str,
    ) -> None:
        """
        Saves the assistant's response to the conversation after streaming.
        """

        conversation.add_message_from_assistant(content)
        await self._repository.save(conversation)

    async def get_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        """
        Retrieve an existing conversation.
        """

        return await self._repository.get(conversation_id)

    async def _get_or_create_conversation(
        self,
        conversation_id: UUID | None,
    ) -> Conversation:
        """
        Retrieves an existing conversation or creates a new one.
        """

        if conversation_id:
            conversation = await self._repository.get(conversation_id)
            if conversation:
                return conversation

        return Conversation(
            title="Chat",
            system_prompt=self._command._system_prompt,
        )

    @staticmethod
    def _generate_title(message: str) -> str:
        """
        Generate a conversation title from the first user message.
        Truncates to ~50 chars at a word boundary.
        """

        title = message.strip().replace("\n", " ")

        if len(title) <= 50:
            return title

        truncated = title[:50].rsplit(" ", 1)[0]
        return f"{truncated}..."

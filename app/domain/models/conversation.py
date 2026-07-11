from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import Field

from app.domain.models.entity import Entity
from app.domain.models.enums import MessageRole
from app.domain.models.message import Message


class Conversation(Entity):
    """
    Represents a chat conversation.
    """

    id: UUID = Field(default_factory=uuid4)

    title: str

    system_prompt: str | None = None

    messages: list[Message] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    def add_message(
        self,
        message: Message,
    ) -> None:
        """
        Add a message to the conversation.
        """

        self.messages.append(message)
        self.updated_at = datetime.now(UTC)

    def add_message_from_user(
        self,
        content: str,
    ) -> None:
        """
        Create and add a user message.
        """

        self.add_message(
            Message(
                role=MessageRole.USER,
                content=content,
            ),
        )

    def add_message_from_assistant(
        self,
        content: str,
    ) -> None:
        """
        Create and add an assistant message.
        """

        self.add_message(
            Message(
                role=MessageRole.ASSISTANT,
                content=content,
            ),
        )

    def rename(
        self,
        title: str,
    ) -> None:
        """
        Rename the conversation.
        """

        self.title = title
        self.updated_at = datetime.now(UTC)

    def message_count(self) -> int:
        """
        Return the number of messages.
        """

        return len(self.messages)

    def is_empty(self) -> bool:
        """
        Return True when the conversation has no messages.
        """

        return len(self.messages) == 0

    def last_message(self) -> Message | None:
        """
        Return the last message or None.
        """

        if self.is_empty():
            return None

        return self.messages[-1]

    def get_messages_for_llm(
        self,
        max_messages: int | None = None,
    ) -> list[Message]:
        """
        Return messages formatted for LLM submission,
        including the system prompt as the first message.

        Optionally truncates to keep the most recent messages
        (always preserving the system prompt).
        """

        messages: list[Message] = []

        if self.system_prompt:
            messages.append(
                Message(
                    role=MessageRole.SYSTEM,
                    content=self.system_prompt,
                )
            )

        conversation_messages = self.messages

        if max_messages and len(conversation_messages) > max_messages:
            conversation_messages = conversation_messages[-max_messages:]

        messages.extend(conversation_messages)

        return messages

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import ConfigDict, Field

from app.domain.models.enums import MessageRole
from app.domain.models.value_object import ValueObject


class Message(ValueObject):
    """
    Represents a message exchanged during a conversation.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(default_factory=uuid4)

    role: MessageRole

    content: str = Field(
        min_length=1,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

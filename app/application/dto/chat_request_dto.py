from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequestDTO(BaseModel):
    """
    Incoming chat request.
    """

    message: str = Field(min_length=1)

    conversation_id: UUID | None = Field(
        default=None,
        description="Existing conversation ID to continue. Omit to start a new conversation.",
    )

    stream: bool = Field(
        default=False,
        description="Whether to stream the response via SSE.",
    )

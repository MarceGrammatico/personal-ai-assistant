from uuid import UUID

from pydantic import BaseModel


class UsageDTO(BaseModel):
    """Token usage information."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponseDTO(BaseModel):
    """
    Chat response returned to the client.
    """

    answer: str

    conversation_id: UUID

    usage: UsageDTO | None = None

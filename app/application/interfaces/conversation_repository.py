from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models import Conversation


class ConversationRepository(ABC):
    """
    Contract for conversation persistence.

    Implementations can be in-memory, Redis, database, etc.
    """

    @abstractmethod
    async def get(self, conversation_id: UUID) -> Conversation | None:
        """Retrieve a conversation by ID."""

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """Persist a conversation."""

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> None:
        """Delete a conversation."""

from uuid import UUID

from app.application.interfaces.conversation_repository import ConversationRepository
from app.domain.models import Conversation


class InMemoryConversationRepository(ConversationRepository):
    """
    In-memory implementation of ConversationRepository.

    Suitable for development and single-instance deployments.
    Replace with Redis/DB implementation for production.
    """

    def __init__(self) -> None:
        self._store: dict[UUID, Conversation] = {}

    async def get(self, conversation_id: UUID) -> Conversation | None:
        return self._store.get(conversation_id)

    async def save(self, conversation: Conversation) -> None:
        self._store[conversation.id] = conversation

    async def delete(self, conversation_id: UUID) -> None:
        self._store.pop(conversation_id, None)

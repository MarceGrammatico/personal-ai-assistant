import pytest

from app.domain.models import Conversation
from app.infrastructure.persistence import InMemoryConversationRepository


@pytest.mark.anyio
async def test_should_save_and_retrieve_conversation():
    repo = InMemoryConversationRepository()
    conversation = Conversation(title="Test")

    await repo.save(conversation)

    retrieved = await repo.get(conversation.id)

    assert retrieved is not None
    assert retrieved.id == conversation.id
    assert retrieved.title == "Test"


@pytest.mark.anyio
async def test_should_return_none_for_unknown_id():
    repo = InMemoryConversationRepository()
    conversation = Conversation(title="Test")

    result = await repo.get(conversation.id)

    assert result is None


@pytest.mark.anyio
async def test_should_delete_conversation():
    repo = InMemoryConversationRepository()
    conversation = Conversation(title="Test")

    await repo.save(conversation)
    await repo.delete(conversation.id)

    result = await repo.get(conversation.id)

    assert result is None

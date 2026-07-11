import pytest

from app.domain.models import Conversation, MessageRole
from app.infrastructure.persistence import SQLiteConversationRepository


@pytest.fixture
def sqlite_repo(tmp_path):
    """Create a SQLite repo with a temp database."""
    db_path = str(tmp_path / "test.db")
    return SQLiteConversationRepository(db_path=db_path)


@pytest.mark.anyio
async def test_should_save_and_retrieve_conversation(sqlite_repo):
    conversation = Conversation(
        title="Test",
        system_prompt="You are helpful.",
    )
    conversation.add_message_from_user("Hello")
    conversation.add_message_from_assistant("Hi there!")

    await sqlite_repo.save(conversation)

    retrieved = await sqlite_repo.get(conversation.id)

    assert retrieved is not None
    assert retrieved.id == conversation.id
    assert retrieved.title == "Test"
    assert retrieved.system_prompt == "You are helpful."
    assert retrieved.message_count() == 2
    assert retrieved.messages[0].role == MessageRole.USER
    assert retrieved.messages[0].content == "Hello"
    assert retrieved.messages[1].role == MessageRole.ASSISTANT
    assert retrieved.messages[1].content == "Hi there!"


@pytest.mark.anyio
async def test_should_return_none_for_unknown_id(sqlite_repo):
    conversation = Conversation(title="Test")

    result = await sqlite_repo.get(conversation.id)

    assert result is None


@pytest.mark.anyio
async def test_should_delete_conversation(sqlite_repo):
    conversation = Conversation(title="Test")
    conversation.add_message_from_user("Hello")

    await sqlite_repo.save(conversation)
    await sqlite_repo.delete(conversation.id)

    result = await sqlite_repo.get(conversation.id)

    assert result is None


@pytest.mark.anyio
async def test_should_update_existing_conversation(sqlite_repo):
    conversation = Conversation(title="Test")
    conversation.add_message_from_user("Hello")

    await sqlite_repo.save(conversation)

    # Add another message and save again
    conversation.add_message_from_assistant("Hi!")
    await sqlite_repo.save(conversation)

    retrieved = await sqlite_repo.get(conversation.id)

    assert retrieved is not None
    assert retrieved.message_count() == 2


@pytest.mark.anyio
async def test_should_persist_across_instances(tmp_path):
    db_path = str(tmp_path / "persist.db")

    # First instance: save
    repo1 = SQLiteConversationRepository(db_path=db_path)
    conversation = Conversation(title="Persistent")
    conversation.add_message_from_user("Remember me")
    await repo1.save(conversation)

    # Second instance: retrieve
    repo2 = SQLiteConversationRepository(db_path=db_path)
    retrieved = await repo2.get(conversation.id)

    assert retrieved is not None
    assert retrieved.title == "Persistent"
    assert retrieved.messages[0].content == "Remember me"


@pytest.mark.anyio
async def test_should_list_recent_conversations(sqlite_repo):
    for i in range(5):
        conv = Conversation(title=f"Conv {i}")
        conv.add_message_from_user(f"Message {i}")
        await sqlite_repo.save(conv)

    recent = await sqlite_repo.list_recent(limit=3)

    assert len(recent) == 3
    assert all("id" in c for c in recent)
    assert all("title" in c for c in recent)
    assert all("message_count" in c for c in recent)

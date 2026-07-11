import pytest

from app.application.services import ChatService
from app.infrastructure.llm.fake import FakeLLMProvider
from app.infrastructure.persistence import InMemoryConversationRepository


@pytest.mark.anyio
async def test_chat_service_should_delegate_to_provider():
    provider = FakeLLMProvider()
    repository = InMemoryConversationRepository()

    service = ChatService(
        llm_provider=provider,
        conversation_repository=repository,
    )

    response, conversation = await service.chat("Hello")

    assert response.message.content == "Hello! I am a fake assistant."
    assert response.usage.total_tokens == 30


@pytest.mark.anyio
async def test_chat_service_should_persist_conversation():
    provider = FakeLLMProvider()
    repository = InMemoryConversationRepository()

    service = ChatService(
        llm_provider=provider,
        conversation_repository=repository,
    )

    response, conversation = await service.chat("Hello")

    # Verify conversation was persisted
    stored = await repository.get(conversation.id)
    assert stored is not None
    assert stored.message_count() == 2  # user + assistant
    assert stored.messages[0].content == "Hello"
    assert stored.messages[1].content == "Hello! I am a fake assistant."


@pytest.mark.anyio
async def test_chat_service_should_continue_existing_conversation():
    provider = FakeLLMProvider()
    repository = InMemoryConversationRepository()

    service = ChatService(
        llm_provider=provider,
        conversation_repository=repository,
    )

    # First message
    _, conversation = await service.chat("Hello")
    conversation_id = conversation.id

    # Second message in same conversation
    _, conversation2 = await service.chat(
        "How are you?",
        conversation_id=conversation_id,
    )

    assert conversation2.id == conversation_id
    # Should have 4 messages: user1, assistant1, user2, assistant2
    assert conversation2.message_count() == 4


@pytest.mark.anyio
async def test_chat_service_should_include_system_prompt():
    provider = FakeLLMProvider()
    repository = InMemoryConversationRepository()

    service = ChatService(
        llm_provider=provider,
        conversation_repository=repository,
    )

    _, conversation = await service.chat("Hello")

    assert conversation.system_prompt is not None
    assert len(conversation.system_prompt) > 0

import pytest

from app.domain.models import ChatRequest, Conversation, LLMModel
from app.infrastructure.llm.fake import FakeLLMProvider


@pytest.mark.anyio
async def test_fake_provider_should_return_chat_response():
    provider = FakeLLMProvider()

    request = ChatRequest(
        conversation=Conversation(
            title="Test",
        ),
        model=LLMModel.FAKE,
    )

    response = await provider.chat(request)

    assert response.message.content == "Hello! I am a fake assistant."

    assert response.usage.total_tokens == 30

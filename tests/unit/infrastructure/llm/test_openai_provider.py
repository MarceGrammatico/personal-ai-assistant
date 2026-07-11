from unittest.mock import AsyncMock, Mock

import pytest

from app.application.exceptions.llm import LLMProviderUnavailable
from app.domain.models import (
    ChatRequest,
    ChatResponse,
    Conversation,
    LLMModel,
)
from app.infrastructure.llm.openai.exceptions import OpenAIRequestError
from app.infrastructure.llm.openai.openai_provider import OpenAIProvider


def _make_completion_mock(content="Hello human"):
    """Create a mock ChatCompletion with no tool calls."""
    choice = Mock()
    choice.message.role = "assistant"
    choice.message.content = content
    choice.message.tool_calls = None

    completion = Mock()
    completion.choices = [choice]
    completion.usage = Mock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
    )
    return completion


@pytest.mark.anyio
async def test_should_send_chat_request_using_openai():
    request = ChatRequest(
        conversation=Conversation(title="Test"),
        model=LLMModel.GPT_5_MINI,
    )

    mock_client = Mock()
    mock_client.chat = AsyncMock(return_value=_make_completion_mock())

    mock_mapper = Mock()
    mock_mapper.to_openai_messages.return_value = [{"role": "user", "content": "Hello"}]

    expected_response = Mock(spec=ChatResponse)
    mock_mapper.to_chat_response.return_value = expected_response

    provider = OpenAIProvider(
        client=mock_client,
        mapper=mock_mapper,
    )

    response = await provider.chat(request)

    assert response == expected_response

    mock_client.chat.assert_called_once_with(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": "Hello"}],
        tools=None,
    )


@pytest.mark.anyio
async def test_should_translate_openai_error_to_provider_error():
    request = ChatRequest(
        conversation=Conversation(title="Test"),
        model=LLMModel.GPT_5_MINI,
    )

    mock_client = Mock()
    mock_client.chat = AsyncMock(
        side_effect=OpenAIRequestError("OpenAI failed"),
    )

    mock_mapper = Mock()
    mock_mapper.to_openai_messages.return_value = [{"role": "user", "content": "Hello"}]

    provider = OpenAIProvider(
        client=mock_client,
        mapper=mock_mapper,
    )

    with pytest.raises(LLMProviderUnavailable):
        await provider.chat(request)

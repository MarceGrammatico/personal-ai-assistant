from unittest.mock import Mock

from app.domain.models import (
    ChatRequest,
    Conversation,
    Message,
    MessageRole,
)
from app.infrastructure.llm.openai.mapper import OpenAIMapper


def test_should_map_domain_messages_to_openai_format():
    conversation = Conversation(
        title="Test",
        system_prompt="You are helpful.",
        messages=[
            Message(role=MessageRole.USER, content="Hello"),
        ],
    )

    request = ChatRequest(
        conversation=conversation,
        model="gpt-5-mini",
    )

    mapper = OpenAIMapper()

    result = mapper.to_openai_messages(request)

    assert result == [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello"},
    ]


def test_should_map_messages_without_system_prompt():
    conversation = Conversation(
        title="Test",
        messages=[
            Message(role=MessageRole.USER, content="Hello"),
        ],
    )

    request = ChatRequest(
        conversation=conversation,
        model="gpt-5-mini",
    )

    mapper = OpenAIMapper()

    result = mapper.to_openai_messages(request)

    assert result == [
        {"role": "user", "content": "Hello"},
    ]


def test_should_map_openai_response_to_domain_response():
    completion = Mock()

    completion.choices = [
        Mock(
            message=Mock(
                role="assistant",
                content="Hello human",
            )
        )
    ]

    completion.usage = Mock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
    )

    mapper = OpenAIMapper()

    response = mapper.to_chat_response(completion)

    assert response.message.role == MessageRole.ASSISTANT
    assert response.message.content == "Hello human"
    assert response.usage.prompt_tokens == 10
    assert response.usage.completion_tokens == 5
    assert response.usage.total_tokens == 15

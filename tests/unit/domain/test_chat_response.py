import pytest
from pydantic import ValidationError

from app.domain.models import (
    ChatResponse,
    Message,
    MessageRole,
    Usage,
)


def test_should_create_chat_response():
    message = Message(
        role=MessageRole.ASSISTANT,
        content="Hello!",
    )

    usage = Usage(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )

    response = ChatResponse(
        message=message,
        usage=usage,
    )

    assert response.message == message
    assert response.usage == usage


def test_should_require_message():
    usage = Usage(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )

    with pytest.raises(ValidationError):
        ChatResponse(
            usage=usage,
        )


def test_should_require_usage():
    message = Message(
        role=MessageRole.ASSISTANT,
        content="Hello!",
    )

    with pytest.raises(ValidationError):
        ChatResponse(
            message=message,
        )

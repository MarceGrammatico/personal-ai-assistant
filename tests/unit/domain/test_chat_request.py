import pytest
from pydantic import ValidationError

from app.domain.models import (
    ChatRequest,
    Conversation,
)


def test_should_create_chat_request():
    conversation = Conversation(title="Sprint")

    request = ChatRequest(
        conversation=conversation,
        model="gpt-5",
    )

    assert request.conversation == conversation

    assert request.model == "gpt-5"


def test_should_require_conversation():
    with pytest.raises(ValidationError):
        ChatRequest(
            model="gpt-5",
        )


def test_should_require_model():
    conversation = Conversation(title="Sprint")

    with pytest.raises(ValidationError):
        ChatRequest(
            conversation=conversation,
        )

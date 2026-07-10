"""
Unit tests for the Message domain model.
"""

from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.domain.models import Message, MessageRole


def test_create_message():
    """
    Should create a valid message.
    """

    # Arrange & Act
    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    # Assert
    assert message.role == MessageRole.USER
    assert message.content == "Hello"


def test_message_requires_content():
    """
    Should reject empty content.
    """

    # Arrange / Act / Assert
    with pytest.raises(ValidationError):
        Message(
            role=MessageRole.USER,
            content="",
        )


def test_message_is_immutable():
    """
    Should not allow modifying a message after creation.
    """

    # Arrange
    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    # Act / Assert
    with pytest.raises(ValidationError) as exc_info:
        message.content = "Modified"

    # Assert
    errors = exc_info.value.errors()

    assert errors[0]["type"] == "frozen_instance"


def test_message_rejects_extra_fields():
    """
    Should reject unexpected fields.
    """

    # Arrange / Act / Assert
    with pytest.raises(ValidationError):
        Message(
            role="user",
            content="Hello",
            invalid_field="value",
        )


def test_role_is_converted_to_enum():
    """
    Should convert string roles into MessageRole.
    """

    # Arrange & Act
    message = Message(
        role="assistant",
        content="Hi!",
    )

    # Assert
    assert message.role == MessageRole.ASSISTANT


def test_message_generates_uuid():
    """
    Should automatically generate a UUID.
    """

    # Arrange & Act
    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    # Assert
    assert isinstance(message.id, UUID)


def test_message_generates_created_at():
    """
    Should automatically generate a creation timestamp.
    """

    # Arrange & Act
    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    # Assert
    assert isinstance(message.created_at, datetime)

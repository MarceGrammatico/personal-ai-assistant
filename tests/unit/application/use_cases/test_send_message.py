from unittest.mock import AsyncMock, Mock

import pytest

from app.application.use_cases import SendMessageUseCase
from app.domain.models import ChatResponse, Conversation


@pytest.mark.anyio
async def test_should_delegate_to_chat_service():
    expected_response = Mock(spec=ChatResponse)
    expected_conversation = Conversation(title="Chat")

    service = Mock()
    service.chat = AsyncMock(
        return_value=(expected_response, expected_conversation),
    )

    use_case = SendMessageUseCase(service)

    result = await use_case.execute("Hello")

    assert result.response == expected_response
    assert result.conversation == expected_conversation

    service.chat.assert_awaited_once_with(
        message="Hello",
        conversation_id=None,
    )

from unittest.mock import AsyncMock, Mock

import pytest
from openai import APITimeoutError

from app.infrastructure.llm.openai.client import OpenAIClient
from app.infrastructure.llm.openai.exceptions import (
    OpenAITimeoutError,
)


@pytest.mark.anyio
async def test_should_send_chat_completion_request():
    mock_response = Mock()

    mock_client = Mock()

    mock_client.chat.completions.create = AsyncMock(
        return_value=mock_response,
    )

    client = OpenAIClient(
        client=mock_client,
    )

    response = await client.chat(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
    )

    assert response == mock_response

    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
    )


@pytest.mark.anyio
async def test_should_translate_timeout_error():
    mock_client = Mock()

    mock_client.chat.completions.create = AsyncMock(
        side_effect=APITimeoutError(
            request=Mock(),
        ),
    )

    client = OpenAIClient(
        client=mock_client,
    )

    with pytest.raises(OpenAITimeoutError):
        await client.chat(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        )

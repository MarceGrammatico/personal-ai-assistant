from openai.types.chat import ChatCompletion

from app.core.config import settings
from app.domain.models import (
    ChatRequest,
    ChatResponse,
    Message,
    MessageRole,
    Usage,
)


class OpenAIMapper:
    """
    Maps between domain models and OpenAI API models.
    """

    def to_openai_messages(
        self,
        request: ChatRequest,
    ) -> list[dict[str, str]]:
        """
        Convert domain messages into OpenAI message format.

        Uses get_messages_for_llm which includes system prompt
        and handles truncation.
        """

        messages = request.conversation.get_messages_for_llm(
            max_messages=settings.MAX_CONVERSATION_MESSAGES,
        )

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

    def to_chat_response(
        self,
        completion: ChatCompletion,
    ) -> ChatResponse:
        """
        Convert OpenAI response into domain response.
        """

        choice = completion.choices[0]

        message = Message(
            role=MessageRole(choice.message.role),
            content=choice.message.content or "",
        )

        usage = Usage(
            prompt_tokens=completion.usage.prompt_tokens if completion.usage else 0,
            completion_tokens=completion.usage.completion_tokens if completion.usage else 0,
            total_tokens=completion.usage.total_tokens if completion.usage else 0,
        )

        return ChatResponse(
            message=message,
            usage=usage,
        )

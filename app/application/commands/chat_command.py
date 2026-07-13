from app.core.config import settings
from app.domain.models import (
    ChatRequest,
    Conversation,
    Message,
    MessageRole,
)


class ChatCommand:
    """
    Builds a ChatRequest from a user message and conversation context.
    """

    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
    ) -> None:
        self._model = model or settings.OPENAI_MODEL
        self._system_prompt = system_prompt or settings.SYSTEM_PROMPT

    def create_request(
        self,
        message: str,
        conversation: Conversation | None = None,
    ) -> ChatRequest:
        """
        Creates a ChatRequest.

        If a conversation is provided, adds the user message to it.
        Otherwise, creates a new conversation with system prompt.
        """

        if conversation is None:
            conversation = Conversation(
                title="Chat",
                system_prompt=self._system_prompt,
            )

        conversation.add_message(
            Message(
                role=MessageRole.USER,
                content=message,
            )
        )

        return ChatRequest(
            conversation=conversation,
            model=self._model,
        )

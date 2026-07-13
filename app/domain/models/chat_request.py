from app.domain.models.conversation import Conversation
from app.domain.models.value_object import ValueObject


class ChatRequest(ValueObject):
    """
    Represents a request sent to an LLM.
    """

    conversation: Conversation

    model: str

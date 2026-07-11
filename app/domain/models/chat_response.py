from app.domain.models.message import Message
from app.domain.models.usage import Usage
from app.domain.models.value_object import ValueObject


class ChatResponse(ValueObject):
    """
    Represents a response returned by an LLM.
    """

    message: Message

    usage: Usage

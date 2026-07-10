from enum import StrEnum


class MessageRole(StrEnum):
    """
    Supported message roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

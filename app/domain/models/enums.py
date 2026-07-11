from enum import StrEnum


class MessageRole(StrEnum):
    """
    Supported message roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class LLMModel(StrEnum):
    """
    Supported LLM models.
    """

    FAKE = "fake"

    GPT_5 = "gpt-5"

    GPT_5_MINI = "gpt-5-mini"

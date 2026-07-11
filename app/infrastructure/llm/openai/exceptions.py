class OpenAIProviderException(Exception):
    """
    Base exception for OpenAI infrastructure errors.
    """


class OpenAIClientError(Exception):
    """
    Base exception for OpenAI client errors.
    """


class OpenAITimeoutError(OpenAIClientError):
    """
    Raised when OpenAI request times out.
    """


class OpenAIRequestError(OpenAIClientError):
    """
    Raised when OpenAI returns an API error.
    """

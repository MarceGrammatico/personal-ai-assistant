from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException


class LLMException(AppException):
    """
    Base exception for LLM related errors.
    """


class LLMProviderUnavailable(LLMException):
    """
    Raised when an LLM provider cannot process a request.
    """

    def __init__(
        self,
        message: str = "LLM provider unavailable",
    ) -> None:
        super().__init__(
            code=ErrorCode.LLM_PROVIDER_UNAVAILABLE,
            message=message,
            status_code=503,
        )

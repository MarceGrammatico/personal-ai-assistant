from enum import StrEnum


class ErrorCode(StrEnum):
    """
    Application error codes.

    These codes are stable identifiers used by
    clients, logs and monitoring systems.
    """

    INTERNAL_ERROR = "INTERNAL_ERROR"

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"

    VALIDATION_ERROR = "VALIDATION_ERROR"

    UNAUTHORIZED = "UNAUTHORIZED"

    FORBIDDEN = "FORBIDDEN"

    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

    LLM_PROVIDER_UNAVAILABLE = "LLM_PROVIDER_UNAVAILABLE"

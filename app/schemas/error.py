from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.core.error_codes import ErrorCode


class ErrorDetail(BaseModel):
    """
    Error information.
    """

    code: ErrorCode = Field(
        description="Application error code",
    )

    message: str = Field(
        description="Human readable error message",
    )


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    success: bool = False

    error: ErrorDetail

    request_id: str | None = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

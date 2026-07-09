from app.core.error_codes import ErrorCode


class AppException(Exception):
    """
    Base application exception.

    All business/application exceptions should inherit
    from this class.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 500,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class ResourceNotFoundException(AppException):
    """
    Resource was not found.
    """

    def __init__(
        self,
        message: str = "Resource not found",
    ) -> None:
        super().__init__(
            code=ErrorCode.RESOURCE_NOT_FOUND,
            message=message,
            status_code=404,
        )


class ValidationException(AppException):
    """
    Validation error.
    """

    def __init__(
        self,
        message: str = "Validation error",
    ) -> None:
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            status_code=400,
        )


class UnauthorizedException(AppException):
    """
    Authentication error.
    """

    def __init__(
        self,
        message: str = "Unauthorized",
    ) -> None:
        super().__init__(
            code=ErrorCode.UNAUTHORIZED,
            message=message,
            status_code=401,
        )


class ForbiddenException(AppException):
    """
    Authorization error.
    """

    def __init__(
        self,
        message: str = "Forbidden",
    ) -> None:
        super().__init__(
            code=ErrorCode.FORBIDDEN,
            message=message,
            status_code=403,
        )

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.context import get_request_id
from app.core.error_codes import ErrorCode
from app.core.exceptions import AppException
from app.core.logging import LoggingConfigurator
from app.schemas.error import ErrorDetail, ErrorResponse

logger = LoggingConfigurator.get_logger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Handle controlled application exceptions.
    """

    logger.warning(
        "Application error: %s",
        exc.message,
    )

    response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code=exc.code,
            message=exc.message,
        ),
        request_id=get_request_id(),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(
            mode="json",
        ),
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected exceptions.
    """

    logger.exception(
        "Unexpected application error",
    )

    response = ErrorResponse(
        success=False,
        error=ErrorDetail(
            code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error",
        ),
        request_id=get_request_id(),
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(
            mode="json",
        ),
    )

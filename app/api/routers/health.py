from fastapi import APIRouter, Request

from app.core.logging import LoggingConfigurator
from app.schemas.health import HealthResponse

logger = LoggingConfigurator.get_logger(__name__)

router = APIRouter()


@router.get("/health")
async def health(
    request: Request,
):
    logger.info("Health endpoint called")

    return HealthResponse(status="ok")

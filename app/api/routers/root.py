from fastapi import APIRouter

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException
from app.core.logging import LoggingConfigurator

logger = LoggingConfigurator.get_logger(__name__)

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """
    Application information endpoint.
    """

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@router.get("/boom")
async def boom():
    raise ResourceNotFoundException("Demo exception")

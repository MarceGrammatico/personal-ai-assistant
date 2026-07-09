from fastapi import APIRouter

from app.core.config import settings
from app.core.metadata import get_application_metadata
from app.schemas.system import SystemInfoResponse

router = APIRouter()


@router.get(
    "/info",
    response_model=SystemInfoResponse,
)
async def system_info() -> SystemInfoResponse:
    metadata = get_application_metadata()

    return SystemInfoResponse(
        name=metadata["name"],
        version=metadata["version"],
        environment=settings.ENVIRONMENT.value,
        build_date=metadata["build_date"],
    )

from fastapi import APIRouter

from app.schemas.health import HealthResponse


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
)
async def health_check() -> HealthResponse:
    """
    Basic application health check.
    """

    return HealthResponse(
        status="ok"
    )

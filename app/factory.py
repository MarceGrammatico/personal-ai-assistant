from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.root import router as root_router
from app.core.config import settings


def create_application() -> FastAPI:
    """
    Application factory.

    Creates and configures the FastAPI application.
    """

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    register_routers(application)

    return application


def register_routers(application: FastAPI) -> None:
    """
    Register application routers.
    """

    application.include_router(root_router)
    application.include_router(health_router)

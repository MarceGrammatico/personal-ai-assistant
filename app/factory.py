from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.handlers.exception_handler import (
    app_exception_handler,
    generic_exception_handler,
)
from app.api.middleware.request_context import RequestContextMiddleware
from app.api.routers.chat import router as chat_router
from app.api.routers.health import router as health_router
from app.api.routers.root import router as root_router
from app.api.routers.settings import router as settings_router
from app.api.routers.system import router as system_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging import LoggingConfigurator


def register_middlewares(app: FastAPI) -> None:
    """
    Register all application middlewares.
    """

    app.add_middleware(RequestContextMiddleware)


def create_application() -> FastAPI:
    """
    Application factory.

    Creates and configures the FastAPI application.
    """

    LoggingConfigurator.configure()
    logger = LoggingConfigurator.get_logger(__name__)

    logger.info("Starting Personal AI Assistant...")

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    register_middlewares(application)
    register_exception_handlers(application)
    register_routers(application)

    return application


def register_routers(application: FastAPI) -> None:
    """
    Register application routers.
    """

    application.include_router(root_router)
    application.include_router(health_router)
    application.include_router(system_router)
    application.include_router(chat_router)
    application.include_router(settings_router)

    # Serve frontend static files (must be last to not override API routes)
    application.mount(
        "/app",
        StaticFiles(directory="frontend", html=True),
        name="frontend",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register application exception handlers.
    """

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        generic_exception_handler,
    )

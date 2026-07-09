import logging
import logging.config

from app.core.config import settings


class LoggingConfigurator:
    """
    Configure and provide application loggers.
    """

    _configured = False

    @classmethod
    def configure(cls) -> None:
        if cls._configured:
            return

        logging.config.dictConfig(cls._build_config())

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        return logging.getLogger(name)

    @classmethod
    def _build_config(cls) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": ("%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s")
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL.value,
            },
        }

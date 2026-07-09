from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment, LogFormat, LogLevel


class Settings(BaseSettings):
    APP_NAME: str = "Personal AI Assistant"
    APP_VERSION: str = "0.1.0"

    DEBUG: bool = True

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    LOG_LEVEL: LogLevel = LogLevel.INFO

    LOG_FORMAT: LogFormat = LogFormat.STANDARD

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()

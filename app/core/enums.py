from enum import StrEnum


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(StrEnum):
    STANDARD = "standard"
    JSON = "json"


class LLMProviderType(StrEnum):
    FAKE = "fake"
    OPENAI = "openai"
    OLLAMA = "ollama"


class StorageType(StrEnum):
    MEMORY = "memory"
    SQLITE = "sqlite"

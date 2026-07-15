from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import (
    Environment,
    LLMProviderType,
    LogFormat,
    LogLevel,
    StorageType,
)


class Settings(BaseSettings):
    APP_NAME: str = "Personal AI Assistant"
    APP_VERSION: str = "0.1.0"

    DEBUG: bool = True

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    LOG_LEVEL: LogLevel = LogLevel.INFO

    LOG_FORMAT: LogFormat = LogFormat.STANDARD

    # --- LLM ---

    LLM_PROVIDER: LLMProviderType = LLMProviderType.FAKE

    OPENAI_API_KEY: str = Field(default="")

    OPENAI_MODEL: str = Field(default="gpt-4o-mini")

    OPENAI_TIMEOUT: int = Field(default=60, gt=0)

    # --- Ollama ---

    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL.",
    )

    OLLAMA_MODEL: str = Field(
        default="llama3.1:8b",
        description="Ollama model name (e.g., llama3.1:8b, mistral, qwen2).",
    )

    # --- System Prompt ---

    SYSTEM_PROMPT: str = Field(
        default=(
            "You are a helpful personal AI assistant specialized in "
            "software development workflows. "
            "You are concise, clear, and helpful. "
            "You answer in the same language the user writes to you. "
            "You HAVE access to the internet through your tools. "
            "When the user asks for current information, news, prices, "
            "schedules, or anything that requires up-to-date data, "
            "ALWAYS use the web_search tool to look it up. "
            "Never say you don't have internet access. "
            "When the user asks about Jira issues, tasks, or project "
            "management, use the Jira tools to fetch real data. "
            "Always format Jira issue information clearly with key, "
            "summary, status, and assignee."
        ),
    )

    # --- Storage ---

    STORAGE_TYPE: StorageType = StorageType.SQLITE

    SQLITE_DB_PATH: str = Field(
        default="data/conversations.db",
        description="Path to SQLite database file.",
    )

    # --- Conversation ---

    MAX_CONVERSATION_TOKENS: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens to keep in conversation history before truncating.",
    )

    MAX_CONVERSATION_MESSAGES: int = Field(
        default=50,
        gt=0,
        description="Maximum number of messages to keep in conversation history.",
    )

    # --- Google Calendar ---

    GOOGLE_CALENDAR_ENABLED: bool = Field(
        default=False,
        description="Enable Google Calendar integration.",
    )

    GOOGLE_CALENDAR_CREDENTIALS_PATH: str = Field(
        default="config/google_credentials.json",
        description="Path to Google OAuth2 credentials file.",
    )

    GOOGLE_CALENDAR_TOKEN_PATH: str = Field(
        default="data/google_token.json",
        description="Path to store the OAuth2 token.",
    )

    GOOGLE_DRIVE_ENABLED: bool = Field(
        default=False,
        description="Enable Google Drive integration.",
    )

    GOOGLE_GMAIL_ENABLED: bool = Field(
        default=False,
        description="Enable Gmail integration.",
    )

    GOOGLE_SHEETS_ENABLED: bool = Field(
        default=False,
        description="Enable Google Sheets integration.",
    )

    # --- Jira ---

    JIRA_ENABLED: bool = Field(
        default=False,
        description="Enable Jira integration.",
    )

    JIRA_DOMAIN: str = Field(
        default="",
        description="Jira Cloud domain, e.g., 'your-org.atlassian.net'",
    )

    JIRA_EMAIL: str = Field(
        default="",
        description="Jira account email for authentication.",
    )

    JIRA_API_TOKEN: str = Field(
        default="",
        description="Jira API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()

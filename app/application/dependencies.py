from functools import lru_cache

from app.application.interfaces.conversation_repository import ConversationRepository
from app.application.interfaces.jira_client import JiraClient
from app.application.interfaces.llm_provider import LLMProvider
from app.application.services import ChatService
from app.application.tools import ToolRegistry
from app.application.use_cases import SendMessageUseCase
from app.core.config import settings
from app.core.enums import LLMProviderType, StorageType
from app.infrastructure.llm.fake import FakeLLMProvider
from app.infrastructure.llm.openai import OpenAIProvider
from app.infrastructure.persistence import (
    InMemoryConversationRepository,
    SQLiteConversationRepository,
)


def get_jira_client() -> JiraClient | None:
    """
    Returns the Jira client if configured.
    """

    if not settings.JIRA_ENABLED:
        return None

    from app.infrastructure.jira import AtlassianJiraClient

    return AtlassianJiraClient()


def get_calendar_client():
    """
    Returns the Google Calendar client if configured.
    """

    if not settings.GOOGLE_CALENDAR_ENABLED:
        return None

    from app.infrastructure.google import GoogleCalendarClient

    return GoogleCalendarClient()


def get_drive_client():
    """
    Returns the Google Drive client if configured.
    """

    if not settings.GOOGLE_DRIVE_ENABLED:
        return None

    from app.infrastructure.google import GoogleDriveClient

    return GoogleDriveClient()


def get_tool_registry() -> ToolRegistry:
    """
    Returns the tool registry with enabled integrations.
    """

    return ToolRegistry(
        jira_enabled=settings.JIRA_ENABLED,
        calendar_enabled=settings.GOOGLE_CALENDAR_ENABLED,
        drive_enabled=settings.GOOGLE_DRIVE_ENABLED,
    )


def get_llm_provider() -> LLMProvider:
    """
    Returns the configured LLM provider.
    """

    if settings.LLM_PROVIDER == LLMProviderType.OPENAI:
        return OpenAIProvider(
            tool_registry=get_tool_registry(),
            jira_client=get_jira_client(),
            calendar_client=get_calendar_client(),
            drive_client=get_drive_client(),
        )

    if settings.LLM_PROVIDER == LLMProviderType.OLLAMA:
        from app.infrastructure.llm.ollama import OllamaProvider

        return OllamaProvider(
            tool_registry=get_tool_registry(),
            jira_client=get_jira_client(),
            calendar_client=get_calendar_client(),
            drive_client=get_drive_client(),
        )

    return FakeLLMProvider()


@lru_cache
def get_conversation_repository() -> ConversationRepository:
    """
    Returns the conversation repository (singleton).
    """

    if settings.STORAGE_TYPE == StorageType.SQLITE:
        return SQLiteConversationRepository(
            db_path=settings.SQLITE_DB_PATH,
        )

    return InMemoryConversationRepository()


def get_chat_service() -> ChatService:
    """
    Returns the chat service.
    """

    return ChatService(
        llm_provider=get_llm_provider(),
        conversation_repository=get_conversation_repository(),
    )


def get_send_message_use_case() -> SendMessageUseCase:
    """
    Returns the send message use case.
    """

    return SendMessageUseCase(
        chat_service=get_chat_service(),
    )

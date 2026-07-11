import pytest
from fastapi.testclient import TestClient

from app.application.dependencies import get_conversation_repository
from app.core.config import settings
from app.core.enums import LLMProviderType, StorageType
from app.factory import create_application


@pytest.fixture(autouse=True)
def _force_test_settings():
    """
    Force test-safe settings:
    - LLM_PROVIDER=fake (no real API calls)
    - STORAGE_TYPE=memory (no disk writes during tests)
    """

    original_provider = settings.LLM_PROVIDER
    original_storage = settings.STORAGE_TYPE

    settings.LLM_PROVIDER = LLMProviderType.FAKE
    settings.STORAGE_TYPE = StorageType.MEMORY

    yield

    settings.LLM_PROVIDER = original_provider
    settings.STORAGE_TYPE = original_storage


@pytest.fixture(autouse=True)
def _clear_conversation_cache():
    """
    Clear the conversation repository cache between tests
    so each test gets a fresh store.
    """

    get_conversation_repository.cache_clear()

    yield

    get_conversation_repository.cache_clear()


@pytest.fixture
def app():
    """Create a fresh application instance."""
    return create_application()


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return TestClient(app)

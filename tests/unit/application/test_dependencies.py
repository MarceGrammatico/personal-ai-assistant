from unittest.mock import patch

from app.application.dependencies import get_llm_provider
from app.core.config import settings
from app.core.enums import LLMProviderType
from app.infrastructure.llm.fake import FakeLLMProvider


def test_should_return_fake_provider_when_configured():
    original_provider = settings.LLM_PROVIDER

    try:
        settings.LLM_PROVIDER = LLMProviderType.FAKE

        provider = get_llm_provider()

        assert isinstance(provider, FakeLLMProvider)

    finally:
        settings.LLM_PROVIDER = original_provider


def test_should_return_openai_provider_when_configured():
    original_provider = settings.LLM_PROVIDER

    try:
        settings.LLM_PROVIDER = LLMProviderType.OPENAI

        with patch("app.application.dependencies.OpenAIProvider") as mock_provider:
            provider = get_llm_provider()

            mock_provider.assert_called_once()
            assert provider == mock_provider.return_value

    finally:
        settings.LLM_PROVIDER = original_provider

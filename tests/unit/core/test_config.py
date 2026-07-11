from app.core.config import settings
from app.domain.models import LLMModel


def test_default_llm_model():
    assert settings.OPENAI_MODEL == LLMModel.GPT_5_MINI

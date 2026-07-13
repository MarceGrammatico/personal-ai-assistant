from app.core.config import settings


def test_openai_model_is_configured():
    assert settings.OPENAI_MODEL != ""

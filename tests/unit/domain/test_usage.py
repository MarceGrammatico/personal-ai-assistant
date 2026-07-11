import pytest
from pydantic import ValidationError

from app.domain.models.usage import Usage


def test_should_create_usage():
    usage = Usage(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )

    assert usage.prompt_tokens == 10
    assert usage.completion_tokens == 20
    assert usage.total_tokens == 30


def test_should_not_accept_negative_prompt_tokens():
    with pytest.raises(ValidationError):
        Usage(
            prompt_tokens=-1,
            completion_tokens=20,
            total_tokens=19,
        )


def test_should_not_accept_negative_completion_tokens():
    with pytest.raises(ValidationError):
        Usage(
            prompt_tokens=10,
            completion_tokens=-1,
            total_tokens=9,
        )


def test_should_not_accept_negative_total_tokens():
    with pytest.raises(ValidationError):
        Usage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=-1,
        )


def test_should_validate_total_tokens():
    with pytest.raises(ValidationError):
        Usage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=100,
        )

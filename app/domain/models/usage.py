from __future__ import annotations

from pydantic import Field, model_validator

from app.domain.models.value_object import ValueObject


class Usage(ValueObject):
    """
    Token usage returned by an LLM provider.
    """

    prompt_tokens: int = Field(ge=0)

    completion_tokens: int = Field(ge=0)

    total_tokens: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_total_tokens(self) -> Usage:
        expected = self.prompt_tokens + self.completion_tokens

        if self.total_tokens != expected:
            raise ValueError("total_tokens must equal prompt_tokens + completion_tokens")

        return self

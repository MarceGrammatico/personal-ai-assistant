from pydantic import ConfigDict

from app.domain.models.base import DomainModel


class ValueObject(DomainModel):
    """
    Immutable value object.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

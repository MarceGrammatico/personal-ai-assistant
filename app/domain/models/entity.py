from pydantic import ConfigDict

from app.domain.models.base import DomainModel


class Entity(DomainModel):
    """
    Mutable domain entity.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

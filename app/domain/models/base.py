from pydantic import BaseModel, ConfigDict


class DomainModel(BaseModel):
    """
    Base class for all domain models.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

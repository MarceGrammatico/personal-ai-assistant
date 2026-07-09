from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str

    service: str

    version: str

    timestamp: datetime

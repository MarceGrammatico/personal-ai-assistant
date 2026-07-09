from datetime import datetime

from pydantic import BaseModel


class SystemInfoResponse(BaseModel):
    name: str

    version: str

    environment: str

    build_date: datetime

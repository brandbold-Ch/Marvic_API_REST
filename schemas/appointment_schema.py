from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

status_choices = ["pending", "completed", "canceled"]


class AppointmentSchema(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(
        ZoneInfo("America/Mexico_City")
    ))
    timestamp: datetime
    issue: str = None
    status: str = Field(default="pending")

    class Config:
        from_attributes = True

    @field_validator("status", mode="after")
    def status_validator(cls, status: str):
        if status in status_choices:
            return status
        raise ValueError(f"Invalid status: {status}. Must be one of {status_choices}.")

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from datetime import datetime

status_choices = ["pending", "completed", "canceled"]


class AppointmentSchema(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(
        ZoneInfo("America/Mexico_City")
    ), validate_default=True)
    timestamp: datetime
    issue: str = None
    status: str = Field(default="pending")
    price: float = Field(default=0.0, validate_default=True)

    class Config:
        from_attributes = True

    @field_validator("status", mode="after")
    def status_validator(cls, status: str):
        if status in status_choices:
            return status
        raise ValueError(f"Invalid status: {status}. Must be one of {status_choices}.")
    
    @field_validator("price", mode="after")
    def price_validator(cls, price: float):
        ctx_time = datetime.now(ZoneInfo("America/Mexico_City")).time()
        
        if (
            (time(9, 0, 0) <= ctx_time <= time(14, 0, 0)) or 
            (time(16, 0, 0) <= ctx_time <= time(19, 0, 0))
        ):
            price = 200
            return price
        else:
            price = 500
            return price
    
    @field_validator("timestamp", mode="after")
    def timestamp_validator(cls, timestamp: datetime):
        return timestamp

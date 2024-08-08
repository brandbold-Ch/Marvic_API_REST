from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4


status_choices = ["pending", "completed", "canceled"]


class Appointment(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    creation_date: datetime = Field(default=datetime.now())
    expiration_date: datetime
    issue: str = None
    status: str = Field(default="pending")
    price: float = Field(default=200.0)

    class Config:
        from_attributes = True

    @field_validator("status", mode="after")
    def status_validator(cls, status: str):
        if status in status_choices:
            return status
        
    @field_validator("price", mode="after")
    def price_validator(cls, price: float):
        if isinstance(price, float):
            return price

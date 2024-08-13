from pydantic import BaseModel, field_validator, Field
from uuid import uuid4, UUID


class User(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=10, min_length=10)

    @field_validator("phone_number", mode="after")
    def phone_number_validator(cls, passwd: str) -> str:
        if passwd.isdigit():
            return passwd
        raise ValueError("Must be a numeric string")

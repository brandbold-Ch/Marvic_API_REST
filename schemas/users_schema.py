from pydantic import BaseModel, field_validator, Field
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = Field(default=uuid4())
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    phone_number: str = Field(max_length=10, min_length=10)

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(uuid4()),
                "name": "John Doe",
                "lastname": "Katerina Koslova",
                "phone_number": "9617105170"
            }
        }

    @field_validator("phone_number", mode="after")
    def phone_number_validator(cls, pn: str) -> str | ValueError:
        if pn.isdigit():
            return pn
        raise ValueError("Must be a numeric string")

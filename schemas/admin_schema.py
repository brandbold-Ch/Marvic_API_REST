from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class AdminSchema(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    occupation: str | None = Field(max_length=60)

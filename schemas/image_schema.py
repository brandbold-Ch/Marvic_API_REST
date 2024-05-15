from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Image(BaseModel):
    id: UUID = Field(default=uuid4())
    image: str = None
    pet_id: UUID = None
    medical_history_id: UUID = None

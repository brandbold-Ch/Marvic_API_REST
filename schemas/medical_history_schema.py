from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class MedicalHistory(BaseModel):
    id: UUID = Field(default=uuid4())
    issue: str = None
    pet_id: UUID

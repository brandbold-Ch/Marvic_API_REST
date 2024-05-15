from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Document(BaseModel):
    id: UUID = Field(default=uuid4())
    document: str = None
    medical_history_id: UUID

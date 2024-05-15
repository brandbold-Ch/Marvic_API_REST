from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class Quote(BaseModel):
    id: UUID = Field(default=uuid4())
    creation_date: datetime = Field(default=datetime.now())
    expiration_date: datetime
    pet_id: UUID
    issue: str = None
    solved: bool = Field(default=False)

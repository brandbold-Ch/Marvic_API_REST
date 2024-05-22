from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class Quote(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    creation_date: datetime = Field(default=datetime.now())
    expiration_date: datetime
    issue: str = None
    solved: bool = Field(default=False)

    class Config:
        from_attributes = True

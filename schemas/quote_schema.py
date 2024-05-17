from pydantic import BaseModel, Field
from datetime import datetime


class Quote(BaseModel):
    creation_date: datetime = Field(default=datetime.now())
    expiration_date: datetime
    issue: str = None
    solved: bool = Field(default=False)

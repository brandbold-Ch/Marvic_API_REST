from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
from uuid import uuid4, UUID
import os

load_dotenv()


class AdminSchema(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    occupation: str = Field(max_length=60)
    trust_key: str = Field(max_length=50, min_length=50)

    @field_validator("trust_key", mode="after")
    def compare_key_trust(cls, key: str):
        if cls.trust_key == os.getenv("TRUST_KEY"):
            delattr(cls, "trust_key")
        else:
            raise Exception("You do not have permission to be an administrator")

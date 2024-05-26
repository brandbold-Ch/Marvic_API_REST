from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import uuid4, UUID
import bcrypt


class Auth(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    email: EmailStr
    password: str

    @field_validator("password", mode="after")
    def password_validator(cls, pwd: str) -> str:
        return bcrypt.hashpw(
            pwd.encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import uuid4, UUID
import bcrypt


class Auth(BaseModel):
    id: UUID = Field(default=uuid4())
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "example_pwd",
            }
        }

    @field_validator("password", mode="after")
    def password_validator(cls, pwd: str) -> str | ValueError:
        return bcrypt.hashpw(
            pwd.encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import uuid4, UUID
import bcrypt

role_choices: list = ["USER", "ADMINISTRATOR"]


class Auth(BaseModel):
    id: UUID = Field(default=uuid4())
    user_id: UUID
    email: EmailStr
    password: str = Field(ge=8)
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(uuid4()),
                "user_id": str(uuid4()),
                "email": "example@gmail.com",
                "password": "example_pwd",
                "role": "USER"
            }
        }

    @field_validator("password", mode="after")
    def password_validator(cls, pwd: str) -> str | ValueError:
        return bcrypt.hashpw(
            pwd.encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

    @field_validator("role", mode="after")
    def role_validator(cls, role: str) -> str | ValueError:
        if role in role_choices:
            return role
        raise ValueError(f"Must be one of the following values {role_choices}")

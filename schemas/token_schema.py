from pydantic import BaseModel, field_validator, Field


class Token(BaseModel):
    access_token: str
    user_id: str
    role: str
    

class TokenData(BaseModel):
    user_id: str
    email: str
    
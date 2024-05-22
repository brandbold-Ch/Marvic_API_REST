from schemas.user_schema import User
from schemas.auth_schema import Auth
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_create_user_data(request: Request) -> tuple:
    try:
        all_data: dict = await request.json()
        user = User(**all_data["user_data"])
        auth = Auth(**all_data["auth_data"])
        return all_data["user_data"], all_data["auth_data"]

    except ValidationError:
        raise ValidationError

    except KeyError:
        raise KeyError


async def validate_update_user_data(request: Request) -> dict:
    try:
        user_data: dict = await request.json()
        user = User(**user_data)
        return user_data

    except ValidationError:
        raise ValidationError

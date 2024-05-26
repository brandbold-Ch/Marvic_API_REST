from errors.exception_classes import ErrorInFields
from schemas.user_schema import User
from schemas.auth_schema import Auth
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_create_user_data(request: Request) -> tuple[dict, dict]:
    try:
        user_data: dict = await request.json()
        name = user_data.get('name')
        lastname = user_data.get('lastname')
        phone_number = user_data.get('phone_number')
        email = user_data.get('email')
        password = user_data.get('password')

        user = User(name=name, lastname=lastname, phone_number=phone_number)
        auth = Auth(email=email, password=password)
        return user.model_dump(), auth.model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)


async def validate_update_user_data(request: Request) -> dict:
    try:
        user_data: dict = await request.json()
        user = User(**user_data)
        return user.dict()

    except ValidationError as error:
        raise ErrorInFields(error)

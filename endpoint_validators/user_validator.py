from errors.exception_classes import ErrorInFields
from schemas.user_schema import User
from schemas.auth_schema import Auth
from pydantic import ValidationError


def validate_create_user_data(request_data: dict[dict, dict]) -> tuple[dict, dict]:
    try:
        return (
            User(**request_data["user_data"]).model_dump(), 
            Auth(**request_data["auth_data"], role="USER").model_dump()
        )
    except ValidationError as error:
        raise ErrorInFields(error)


def validate_update_user_data(request_data: dict) -> dict:
    try:
        return User(**request_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

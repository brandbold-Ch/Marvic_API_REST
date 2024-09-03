from errors.exception_classes import DataValidationError
from schemas.user_schema import User
from schemas.auth_schema import Auth
from pydantic import ValidationError
from typing import Annotated
from fastapi import Body


def validate_create(
        name: Annotated[str, Body(...)],
        lastname: Annotated[str, Body(...)],
        phone_number: Annotated[str, Body(...)],
        email: Annotated[str, Body(...)],
        password: Annotated[str, Body(...)]
) -> tuple[dict, dict]:
    try:
        return (
            User(
                name=name,
                lastname=lastname,
                phone_number=phone_number
            ).model_dump(),
            Auth(
                email=email,
                password=password,
                role="USER"
            ).model_dump()
        )
    except ValidationError as e:
        raise DataValidationError(e)


def validate_update(
        name: Annotated[str, Body(...)],
        lastname: Annotated[str, Body(...)],
        phone_number: Annotated[str, Body(...)]
) -> dict:
    try:
        return User(
            name=name,
            lastname=lastname,
            phone_number=phone_number
        ).model_dump()

    except ValidationError as e:
        raise DataValidationError(e)

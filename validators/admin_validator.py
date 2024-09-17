from errors.exception_classes import DataValidationError
from schemas.admin_schema import AdminSchema
from schemas.auth_schema import AuthSchema
from pydantic import ValidationError
from typing import Annotated
from fastapi import Body


def validate_create(
    name: str,
    lastname: str,
    email: str,
    password: str,
    occupation: str = None,
) -> dict[dict, dict]:
    try:
        return (
            AdminSchema(
                name=name,
                lastname=lastname,
                occupation=occupation
            ).model_dump(),
            AuthSchema(
                email=email,
                password=password,
                role="ADMINISTRATOR"
            ).model_dump()
        )
        
    except ValidationError as e:
        raise DataValidationError(e) from e

def validate_update(
    name: Annotated[str, Body(...)],
    lastname: Annotated[str, Body(...)],
    occupation: Annotated[str, Body(...)] = None
) -> dict:
    try:
        return AdminSchema(
            name=name,
            lastname=lastname,
            occupation=occupation
        ).model_dump()
        
    except ValidationError as e:
        raise DataValidationError(e) from e

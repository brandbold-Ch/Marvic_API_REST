from errors.exception_classes import ErrorInFields
from pydantic import ValidationError
from schemas.pet_schema import Pet


def validate_create_pet_data(request_data: dict) -> dict:
    try:
        return Pet(**request_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

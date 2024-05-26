from errors.exception_classes import ErrorInFields
from schemas.pet_schema import Pet
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_create_pet_data(request: Request) -> dict:
    try:
        form_data = await request.form()
        pet_data = dict(form_data.items())
        return Pet(**pet_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

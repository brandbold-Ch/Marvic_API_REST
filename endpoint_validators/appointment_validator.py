from errors.exception_classes import ErrorInFields
from schemas.appointment_schema import Appointment
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_create_appointment_data(request: Request) -> dict:
    try:
        quote_data = await request.json()
        return Appointment(**quote_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

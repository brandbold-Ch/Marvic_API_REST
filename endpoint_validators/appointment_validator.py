from errors.exception_classes import ErrorInFields
from schemas.appointment_schema import Appointment
from pydantic import ValidationError


async def validate_create_appointment_data(request) -> dict:
    try:
        quote_data = await request.json()
        return Appointment(**quote_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

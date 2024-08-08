from errors.exception_classes import ErrorInFields
from schemas.appointment_schema import Appointment
from pydantic import ValidationError


def validate_create_appointment_data(request_data: dict) -> dict:
    try:
        return Appointment(**request_data).model_dump()

    except ValidationError as error:
        raise ErrorInFields(error)

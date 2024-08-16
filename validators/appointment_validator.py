from errors.exception_classes import ErrorInFields
from schemas.appointment_schema import Appointment
from pydantic import ValidationError
from datetime import datetime
from typing import Annotated
from fastapi import Body


def validate_create(
        expiration_date: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None,
        price: Annotated[float, Body(...)] = None
) -> dict:
    try:
        return Appointment(
            expiration_date=expiration_date,
            issue=issue,
            price=price
        ).model_dump()

    except ValidationError as e:
        raise ErrorInFields(e)

from errors.exception_classes import DataValidationError
from schemas.appointment_schema import Appointment
from pydantic import ValidationError
from datetime import datetime
from typing import Annotated
from fastapi import Body


def validate_create(
        timestamp: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None,
        price: Annotated[float, Body(...)] = None
) -> dict:
    try:
        return Appointment(
            timestamp=timestamp,
            issue=issue,
            price=price
        ).model_dump()

    except ValidationError as e:
        raise DataValidationError(e)

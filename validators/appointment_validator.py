from errors.exception_classes import DataValidationError, ServerUnknownError
from schemas.appointment_schema import AppointmentSchema
from pydantic import ValidationError
from datetime import datetime
from typing import Annotated
from fastapi import Body


def validate_create(
        timestamp: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None,
) -> dict:
    try:
        return AppointmentSchema(
            timestamp=timestamp,
            issue=issue,
        ).model_dump()

    except ValidationError as e:
        raise DataValidationError(e) from e

    except Exception as e:
        raise ServerUnknownError(detail=e) from e

from errors.exception_classes import InvalidId, DoesNotExistInDatabase
from endpoint_validators.appointment_validator import validate_create
from controllers.appointment_controller import AppointmentControllers
from errors.http_error_handler import HandlerResponses
from fastapi import APIRouter, Path, Depends, status
from utils.status_codes import error_codes
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from typing import Annotated, Any


appointment_routes = APIRouter()
appointment_controller = AppointmentControllers(SessionLocal())


@appointment_routes.post("/")
async def create_appointment(
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)],
        appointment_data=Depends(validate_create)
) -> JSONResponse:
    result: dict = appointment_controller.create_appointment(
        user_id, pet_id, appointment_data
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "Created 🆕",
            "message": "Created appointment ✅",
            "codes": {
                "status_code": status.HTTP_201_CREATED,
            },
            "data": result
        }
    )


@appointment_routes.get("/")
async def get_appointments(
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
) -> list[dict] | Any:
    try:
        return appointment_controller.get_appointments(user_id, pet_id)

    except InvalidId as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), error_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), error_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), error_codes["SERVER_UNKNOWN_ERROR"])
        )


@appointment_routes.get("/{appointment_id}")
async def get_appointment(
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> dict | Any:
    try:
        return appointment_controller.get_appointment(user_id, pet_id, appointment_id)

    except InvalidId as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), error_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), error_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), error_codes["SERVER_UNKNOWN_ERROR"])
        )


@appointment_routes.delete("/{appointment_id}")
async def delete_appointment(
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    try:
        appointment_controller.delete_appointment(user_id, pet_id, appointment_id)
        return JSONResponse(status_code=204, content=None)

    except InvalidId as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), error_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), error_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), error_codes["SERVER_UNKNOWN_ERROR"])
        )

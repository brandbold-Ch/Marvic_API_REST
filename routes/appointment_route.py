from errors.exception_classes import ErrorInFields, InvalidUUID, DoesNotExistInDatabase
from endpoint_validators.appointment_validator import validate_create_appointment_data
from fastapi import APIRouter, Path
from endpoint_validators.user_validator import Request
from controllers.appointment_controller import AppointmentControllers
from fastapi import Body
from errors.http_error_handler import HandlerResponses
from fastapi.encoders import jsonable_encoder
from utils.status_codes import errors_codes
from fastapi.responses import JSONResponse
from typing import Annotated, Any
from datetime import datetime

appointments = APIRouter()
appointment_controller = AppointmentControllers()


@appointments.post("/")
async def create_appointment(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        expiration_date: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None,
        status: Annotated[str, Body(...)] = None,
        price: Annotated[float, Body(...)]  = None
) -> JSONResponse:
    try:
        appointment_data: dict = await validate_create_appointment_data(request)
        appointment_controller.create_appointment(user_id, pet_id, appointment_data)
        
        return JSONResponse(
            status_code=201,
            content=HandlerResponses.created("Created quote", data=jsonable_encoder(appointment_data))
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["JSON_INVALID_DATA_TYPE"])
        )
    
    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@appointments.get("/")
async def get_appointments(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
) -> list[dict] | Any:
    try:
        return appointment_controller.get_appointments(user_id, pet_id)

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@appointments.get("/{appointment_id}")
async def get_appointment(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> dict | Any:
    try:
        return appointment_controller.get_appointment(user_id, appointment_id, pet_id)

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@appointments.delete("/{appointment_id}")
async def delete_appointment(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    try:
        appointment_controller.delete_appointment(user_id, appointment_id, pet_id)
        return JSONResponse(status_code=204, content=None)

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )

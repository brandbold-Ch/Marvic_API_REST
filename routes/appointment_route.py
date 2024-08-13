from errors.exception_classes import ErrorInFields, InvalidId, DoesNotExistInDatabase
from endpoint_validators.appointment_validator import validate_create_appointment_data
from controllers.appointment_controller import AppointmentControllers
from errors.http_error_handler import HandlerResponses
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from utils.status_codes import error_codes
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from fastapi import APIRouter, Path
from typing import Annotated, Any
from datetime import datetime
from fastapi import Body


appointment_routes = APIRouter()
appointment_controller = AppointmentControllers(SessionLocal())


@appointment_routes.post("/")
async def create_appointment(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)],
        expiration_date: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None,
        price: Annotated[float, Body(...)] = None
) -> JSONResponse:
    try:
        appointment_data: dict = appointment_controller.create_appointment(
            user_id,
            pet_id,
            validate_create_appointment_data({
                "user_id": user_id,
                "pet_id": pet_id,
                "expiration_date": expiration_date,
                "issue": issue,
                "price": price
            })
        )
        
        return JSONResponse(
            status_code=201,
            content=HandlerResponses.created("Created quote", data=appointment_data)
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), error_codes["JSON_INVALID_DATA_TYPE"])
        )
    
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


@appointment_routes.get("/")
async def get_appointments(
        request: Request,
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
        request: Request,
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
        request: Request,
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

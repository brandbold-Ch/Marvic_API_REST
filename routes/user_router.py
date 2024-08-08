from endpoint_validators.user_validator import validate_create_user_data, validate_update_user_data
from controllers.user_controller import UserControllers
from errors.http_error_handler import HandlerResponses
from fastapi import APIRouter, Path, Body, status
from utils.status_codes import errors_codes
from fastapi.responses import JSONResponse
from schemas.user_schema import User
from fastapi.requests import Request
from utils.config_orm import SessionLocal
from typing import Any, Annotated
from errors.exception_classes import (
    DuplicatedInDatabase,
    DoesNotExistInDatabase,
    ErrorInFields,
    InvalidUUID
)
from fastapi import FastAPI


main_app = FastAPI()
users = APIRouter()
user_controller = UserControllers(SessionLocal())
users.add_event_handler

@main_app.get("/")
def test():
    return {"ok": True}

@users.post("/")
async def create_user(
        request: Request,
        name: Annotated[str, Body(...)],
        lastname: Annotated[str, Body(...)],
        phone_number: Annotated[str, Body(...)],
        email: Annotated[str, Body(...)],
        password: Annotated[str, Body(...)]
) -> JSONResponse:
    try:
        result: dict[dict, dict] = user_controller.create_user(
            *validate_create_user_data({
                "user_data": {
                    "name": name, 
                    "lastname": lastname, 
                    "phone_number": phone_number, 
                },
                "auth_data": {
                    "email": email, 
                    "password": password
                }
            })
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=HandlerResponses.created("Created user", data=result)
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=HandlerResponses.unprocessable_entity(str(error), errors_codes["JSON_INVALID_DATA_TYPE"])
        )

    except DuplicatedInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_DUPLICATED_KEY"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@users.put("/{user_id}")
async def update_user(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        name: Annotated[str, Body(...)],
        lastname: Annotated[str, Body(...)],
        phone_number: Annotated[str, Body(...)],
) -> JSONResponse:
    try:
        result: dict = user_controller.update_user(
            validate_update_user_data({
            "name": name, 
            "lastname": lastname, 
            "phone_number": phone_number, 
        }), user_id)
        
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=HandlerResponses.created("Updated user", data=result)
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=HandlerResponses.unprocessable_entity(str(error), errors_codes["JSON_INVALID_DATA_TYPE"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@users.get("/{user_id}")
async def get_user(request: Request, user_id: Annotated[str, Path(max_length=36)]) -> User | Any:
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=user_controller.get_user(user_id)
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@users.delete("/{user_id}")
async def delete_user(request: Request, user_id: Annotated[str, Path(max_length=36)]) -> JSONResponse:
    try:
        user_controller.delete_user(user_id)
        return JSONResponse(status_code=204, content=None)

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )

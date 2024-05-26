from endpoint_validators.user_validator import validate_create_user_data, validate_update_user_data
from controllers.user_controller import UserControllers
from endpoint_validators.user_validator import Request
from errors.http_error_handler import HandlerResponses
from utils.status_codes import errors_codes
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path, Body, status
from schemas.user_schema import User
from typing import Any, Annotated
from errors.exception_classes import (
    DuplicatedInDatabase,
    DoesNotExistInDatabase,
    InvalidUUID,
    ErrorInFields
)

users = APIRouter()
user_controller = UserControllers()


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
        user_data, auth_data = await validate_create_user_data(request)
        user_controller.create_user(user_data, auth_data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=HandlerResponses.created("Created user", data=await request.json())
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
        user_data: dict = await validate_update_user_data(request)
        user_controller.update_user(user_data, user_id)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=HandlerResponses.created("Updated user", data=user_data)
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
        return user_controller.get_user(user_id)

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

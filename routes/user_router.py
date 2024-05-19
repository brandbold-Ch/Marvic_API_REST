from middlewares.user_middleware import validate_create_user_data, validate_update_user_data
from controllers.user_controller import UserControllers
from middlewares.user_middleware import Request
from pydantic import ValidationError
from utils.status_codes import errors_codes
from fastapi import APIRouter, Depends, Path
from errors.exception_classes import DuplicatedInDatabase, DoesNotExistInDatabase, InvalidUUID
from errors.handle_errors import HandleErrors
from fastapi.responses import JSONResponse
from schemas.user_schema import User
from schemas.auth_schema import Auth
from typing import Any

users = APIRouter()
user_controller = UserControllers()


@users.post("/", dependencies=[Depends(validate_create_user_data)])
async def create_user(request: Request, user_data: User, auth_data: Auth) -> JSONResponse:
    try:
        user_controller.create_user(user_data.dict(), auth_data.dict())
        return JSONResponse(
            status_code=201,
            content=HandleErrors.created("Created user", data=await request.json())
        )

    except ValidationError as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["JSON_MISSING_PARAMETERS"])
        )

    except DuplicatedInDatabase as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["DB_DUPLICATED_KEY"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandleErrors.bad_request(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@users.put("/{user_id}", dependencies=[Depends(validate_update_user_data)])
async def update_user(request: Request, user_data: User, user_id: str = Path(...)) -> JSONResponse:
    try:
        user_controller.update_user(user_data.dict(), user_id)
        return JSONResponse(
            status_code=202,
            content=HandleErrors.created("Updated user", data=await request.json())
        )

    except ValidationError as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["JSON_MISSING_PARAMETERS"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandleErrors.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )


@users.get("/{user_id}")
async def get_user(request: Request, user_id: str = Path(...)) -> User | Any:
    try:
        return user_controller.get_user(user_id)

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandleErrors.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandleErrors.bad_request(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@users.delete("/{user_id}")
async def delete_user(request: Request, user_id: str = Path(...)) -> JSONResponse:
    try:
        user_controller.delete_user(user_id)
        return JSONResponse(status_code=204, content=None)

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandleErrors.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandleErrors.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandleErrors.bad_request(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )

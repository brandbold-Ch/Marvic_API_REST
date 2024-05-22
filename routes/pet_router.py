from errors.exception_classes import ErrorInFields, DoesNotExistInDatabase, InvalidUUID
from endpoint_validators.pet_validator import validate_create_pet_data
from fastapi import APIRouter, Path, Form, UploadFile
from endpoint_validators.user_validator import Request
from controllers.pet_controller import PetController
from errors.http_error_handler import HandlerResponses
from fastapi.encoders import jsonable_encoder
from utils.status_codes import errors_codes
from fastapi.responses import JSONResponse
from typing import Any, Annotated


pets = APIRouter()
pet_controller = PetController()


@pets.post("/")
async def create_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        specie: Annotated[str, Form(...)],
        gender: Annotated[str, Form(...)],
        name: Annotated[str, Form(...)] = None,
        size: Annotated[str, Form(...)] = None,
        age: Annotated[str, Form(...)] = None,
        breed: Annotated[str, Form(...)] = None,
        weight: Annotated[float, Form(...)] = None,
        images: Annotated[UploadFile(...), Form(...)] = None
) -> JSONResponse:
    try:
        pet_data: dict = await validate_create_pet_data(request)
        pet_controller.create_pet(user_id, pet_data)

        return JSONResponse(
            status_code=201,
            content=HandlerResponses.created("Created pet", data=jsonable_encoder(pet_data))
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["ERROR_DATA_VALIDATION"])
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


@pets.get("/")
async def get_pets(request: Request, user_id: Annotated[str, Path(max_length=36)]) -> list[dict] | Any:
    try:
        return pet_controller.get_pets(user_id)

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


@pets.get("/{pet_id}")
async def get_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> dict | Any:
    try:
        return pet_controller.get_pet(user_id, pet_id)

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@pets.put("/{pet_id}")
async def update_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)],
        specie: Annotated[str, Form(...)],
        gender: Annotated[str, Form(...)],
        name: Annotated[str, Form(...)] = None,
        size: Annotated[str, Form(...)] = None,
        age: Annotated[str, Form(...)] = None,
        breed: Annotated[str, Form(...)] = None,
        weight: Annotated[float, Form(...)] = None,
        is_live: Annotated[bool, Form()] = None,
        images: Annotated[UploadFile(...), Form(...)] = None
) -> JSONResponse:
    try:
        pet_data: dict = await validate_create_pet_data(request)
        pet_controller.update_pet(user_id, pet_id, pet_data)

        return JSONResponse(
            status_code=202,
            content=HandlerResponses.accepted("Updated pet", data=jsonable_encoder(pet_data))
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["ERROR_DATA_VALIDATION"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@pets.delete("/{pet_id}")
async def get_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    try:
        pet_controller.delete_pet(user_id, pet_id)
        return JSONResponse(status_code=204, content=None)

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=404,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=400,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )
    
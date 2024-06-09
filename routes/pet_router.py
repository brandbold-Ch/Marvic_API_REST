from errors.exception_classes import ErrorInFields, DoesNotExistInDatabase, InvalidUUID
from endpoint_validators.pet_validator import validate_create_pet_data
from fastapi import APIRouter, Path, Form, UploadFile, File, status
from fastapi.requests import Request
from errors.http_error_handler import HandlerResponses
from controllers.pet_controller import PetController
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
        image: Annotated[UploadFile, File()] = None
) -> JSONResponse:
    try:
        request_data: dict = await pet_controller.create_pet(
            user_id, 
            validate_create_pet_data({
                "specie": specie,
                "gender": gender,
                "name": name,
                "size": size,
                "age": age,
                "breed": breed,
                "weight": weight,
                "image": image
            })
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=HandlerResponses.created("Created pet", data=request_data)
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["ERROR_DATA_VALIDATION"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@pets.get("/")
async def get_pets(request: Request, user_id: Annotated[str, Path(max_length=36)]) -> list[dict] | Any:
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=await pet_controller.get_pets(user_id)
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@pets.get("/{pet_id}")
async def get_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> dict | Any:
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=await pet_controller.get_pet(user_id, pet_id)
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        image: Annotated[UploadFile, File()] = None
) -> JSONResponse:
    try:
        pet_data: dict = await validate_create_pet_data(request)
        await pet_controller.update_pet(user_id, pet_id, pet_data)

        return JSONResponse(
            status_code=202,
            content=HandlerResponses.accepted("Updated pet", data=jsonable_encoder(pet_data))
        )

    except ErrorInFields as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["ERROR_DATA_VALIDATION"])
        )

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )


@pets.delete("/{pet_id}")
async def delete_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    try:
        await pet_controller.delete_pet(user_id, pet_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    except InvalidUUID as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=HandlerResponses.bad_request(str(error), errors_codes["DB_INVALID_FORMAT_ID"])
        )

    except DoesNotExistInDatabase as error:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=HandlerResponses.not_found(str(error), errors_codes["DB_NOT_FOUND"])
        )

    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=HandlerResponses.internal_server_error(str(error), errors_codes["SERVER_UNKNOWN_ERROR"])
        )

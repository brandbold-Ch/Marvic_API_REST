from errors.exception_classes import ErrorInFields, InvalidUUID, DoesNotExistInDatabase
from endpoint_validators.quote_validator import validate_create_quote_data
from fastapi import APIRouter, Path
from endpoint_validators.user_validator import Request
from controllers.quote_controller import QuoteControllers
from fastapi import Body
from errors.http_error_handler import HandlerResponses
from fastapi.encoders import jsonable_encoder
from utils.status_codes import errors_codes
from fastapi.responses import JSONResponse
from typing import Annotated, Any
from datetime import datetime

quotes = APIRouter()
quote_controller = QuoteControllers()


@quotes.post("/")
async def create_quote(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        expiration_date: Annotated[datetime, Body(...)],
        issue: Annotated[str, Body(...)] = None
) -> JSONResponse:
    try:
        quote_data: dict = await validate_create_quote_data(request)
        quote_controller.create_quote(user_id, pet_id, quote_data)
        
        return JSONResponse(
            status_code=201,
            content=HandlerResponses.created("Created quote", data=jsonable_encoder(quote_data))
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


@quotes.get("/")
async def get_quotes(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
) -> list[dict] | Any:
    try:
        return quote_controller.get_quotes(user_id, pet_id)

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


@quotes.get("/{quote_id}")
async def get_quote(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        quote_id: Annotated[str, Path(max_length=36)],
) -> dict | Any:
    try:
        return quote_controller.get_quote(user_id, quote_id, pet_id)

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


@quotes.delete("/{quote_id}")
async def delete_quote(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        quote_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    try:
        quote_controller.delete_quotes(user_id, quote_id, pet_id)
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

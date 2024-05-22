from errors.exception_classes import ErrorInFields
from schemas.quote_schema import Quote
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_create_quote_data(request: Request) -> dict:
    try:
        quote_data = await request.json()
        return Quote(**quote_data).dict()

    except ValidationError as error:
        raise ErrorInFields(error)

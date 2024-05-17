from fastapi.responses import JSONResponse
from schemas.users_schema import User
from schemas.auth_schema import Auth
from fastapi.requests import Request
from pydantic import ValidationError


async def validate_user_data(request: Request):
    try:
        all_data: dict = await request.json()
        user = User(**all_data["user_data"])
        auth = Auth(**all_data["auth_data"])
        return all_data["user_data"], all_data["auth_data"]

    except ValidationError as error:
        return JSONResponse(status_code=400, content={"message": str(error)})

from fastapi import APIRouter, Body, Path, status, Query, Depends
from decorators.validator_decorators import authenticate
from controllers.auth_controller import AuthControllers
from utils.token_tools import CustomHTTPBearer
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from fastapi.requests import Request
from typing import Annotated

auth_routes = APIRouter()
auth_controller = AuthControllers(SessionLocal())
bearer = CustomHTTPBearer()


@auth_routes.put("/change-password/{user_id}", dependencies=[Depends(bearer)])
@authenticate
async def update_auth(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        ctx_password: Annotated[str, Body(...)],
        new_password: Annotated[str, Body(...)],
        email: Annotated[str, Body(...)],
        role: Annotated[str, Query(...)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted 🤝",
            "message": "Updated auth ✅",
            "codes": {
                "status_code": status.HTTP_202_ACCEPTED,
            },
            "data": auth_controller.update_auth(
                user_id=user_id,
                ctx_password=ctx_password,
                new_password=new_password,
                email=email,
                role=role
            )
        }
    )


@auth_routes.post("/login")
async def login(
        email: Annotated[str, Body(...)],
        password: Annotated[str, Body(...)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=auth_controller.auth_login(
            email=email,
            password=password
        )
    )

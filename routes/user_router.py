from endpoint_validators.user_validator import validate_create, validate_update
from controllers.user_controller import UserControllers
from fastapi import APIRouter, Path, status, Depends
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from typing import Annotated


user_routes = APIRouter()
user_controller = UserControllers(SessionLocal())


@user_routes.post("/")
async def create_user(user_data=Depends(validate_create)) -> JSONResponse:
    result: dict = user_controller.create_user(*user_data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "Created 🆕",
            "message": "Created user ✅",
            "codes": {
                "status_code": status.HTTP_201_CREATED,
            },
            "data": result
        }
    )


@user_routes.put("/{user_id}")
async def update_user(
        user_id: Annotated[str, Path(max_length=36)],
        user_data=Depends(validate_update)
) -> JSONResponse:
    result: dict = user_controller.update_user(user_id, user_data)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted 🤝",
            "message": "Updated user ✅",
            "codes": {
                "status_code": status.HTTP_202_ACCEPTED,
            },
            "data": result
        }
    )


@user_routes.get("/{user_id}")
async def get_user(user_id: Annotated[str, Path(max_length=36)]) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_controller.get_user(user_id)
    )


@user_routes.delete("/{user_id}")
async def delete_user(user_id: Annotated[str, Path(max_length=36)]) -> JSONResponse:
    user_controller.delete_user(user_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

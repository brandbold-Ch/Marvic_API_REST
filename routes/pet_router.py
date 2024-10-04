from decorators.validator_decorators import authenticate
from controllers.pet_controller import PetController
from fastapi import APIRouter, Path, status, Depends
from validators.pet_validator import validate_data
from utils.token_tools import CustomHTTPBearer
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from fastapi.requests import Request
from typing import Annotated
from fastapi import Depends


pet_routes = APIRouter()
pet_controller = PetController(SessionLocal())
bearer = CustomHTTPBearer()


@pet_routes.post("/", dependencies=[Depends(bearer)])
@authenticate
async def create_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_data=Depends(validate_data)
) -> JSONResponse:
    result: dict = await pet_controller.create_pet(
        user_id=user_id, pet_data=pet_data
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "Created 🆕",
            "message": "Created pet ✅",
            "codes": {
                "status_code": status.HTTP_201_CREATED,
            },
            "data": result
        }
    )


@pet_routes.get("/", dependencies=[Depends(bearer)])
@authenticate
async def get_pets(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=pet_controller.get_pets(user_id=user_id)
    )


@pet_routes.get("/{pet_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=pet_controller.get_pet(
            user_id=user_id, pet_id=pet_id
        )
    )


@pet_routes.put("/{pet_id}", dependencies=[Depends(bearer)])
@authenticate
async def update_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)],
        pet_data=Depends(validate_data)
) -> JSONResponse:
    result = await pet_controller.update_pet(
        user_id=user_id,
        pet_id=pet_id,
        pet_data=pet_data
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted 🤝",
            "message": "Updated pet ✅",
            "codes": {
                "status_code": status.HTTP_202_ACCEPTED,
            },
            "data": result
        }
    )


@pet_routes.delete("/{pet_id}", dependencies=[Depends(bearer)])
@authenticate
async def delete_pet(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    pet_controller.delete_pet(
        user_id=user_id, pet_id=pet_id
    )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@pet_routes.delete("/{pet_id}/image", dependencies=[Depends(bearer)])
@authenticate
async def delete_image(
    request: Request,
    user_id: Annotated[str, Path(max_length=36)],
    pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    pet_controller.delete_image(pet_id=pet_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

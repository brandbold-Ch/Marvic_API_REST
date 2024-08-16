from validators.pet_validator import validate_data
from controllers.pet_controller import PetController
from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from typing import Annotated
from fastapi import Depends


pet_routes = APIRouter()
pet_controller = PetController(SessionLocal())


@pet_routes.post("/")
async def create_pet(
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


@pet_routes.get("/")
async def get_pets(user_id: Annotated[str, Path(max_length=36)]) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=pet_controller.get_pets(user_id=user_id)
    )


@pet_routes.get("/{pet_id}")
async def get_pet(
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=pet_controller.get_pet(
            user_id=user_id, pet_id=pet_id
        )
    )


@pet_routes.put("/{pet_id}")
async def update_pet(
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


@pet_routes.delete("/{pet_id}")
async def delete_pet(
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    pet_controller.delete_pet(
        user_id=user_id, pet_id=pet_id
    )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

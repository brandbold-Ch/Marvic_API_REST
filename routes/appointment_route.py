from controllers.appointment_controller import AppointmentControllers
from validators.appointment_validator import validate_create
from decorators.validator_decorators import authenticate
from fastapi import APIRouter, Path, Depends, status
from utils.token_tools import CustomHTTPBearer
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from fastapi.requests import Request
from typing import Annotated


appointment_routes = APIRouter()
appointment_controller = AppointmentControllers(SessionLocal())
bearer = CustomHTTPBearer()


@appointment_routes.post("/", dependencies=[Depends(bearer)])
@authenticate
async def create_appointment(
        request: Request,
        user_id: Annotated[str, Path(max_length=36)],
        pet_id: Annotated[str, Path(max_length=36)],
        appointment_data=Depends(validate_create)
) -> JSONResponse:
    result: dict = appointment_controller.create_appointment(
        user_id=user_id,
        pet_id=pet_id,
        appointment_data=appointment_data
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "Created 🆕",
            "message": "Created appointment ✅",
            "codes": {
                "status_code": status.HTTP_201_CREATED,
            },
            "data": result
        }
    )


@appointment_routes.get("/", dependencies=[Depends(bearer)])
@authenticate
async def get_appointments(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=appointment_controller.get_appointments(
            user_id=user_id, pet_id=pet_id
        )
    )


@appointment_routes.get("/{appointment_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_appointment(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=appointment_controller.get_appointment(
            user_id=user_id,
            pet_id=pet_id,
            appointment_id=appointment_id
        )
    )


@appointment_routes.delete("/{appointment_id}", dependencies=[Depends(bearer)])
@authenticate
async def delete_appointment(
        request: Request,
        pet_id: Annotated[str, Path(max_length=36)],
        user_id: Annotated[str, Path(max_length=36)],
        appointment_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    appointment_controller.delete_appointment(
        user_id=user_id,
        pet_id=pet_id,
        appointment_id=appointment_id
    )
    return JSONResponse(status_code=204, content=None)

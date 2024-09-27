from validators.admin_validator import validate_update, validate_create
from controllers.admin_controller import AdminControllers
from decorators.validator_decorators import authenticate
from fastapi import Depends, status, Body, Query
from utils.token_tools import CustomHTTPBearer
from fastapi.responses import JSONResponse
from utils.config_orm import SessionLocal
from fastapi.requests import Request
from fastapi import APIRouter, Path
from typing import Annotated


admin = APIRouter()
admin_controller = AdminControllers(SessionLocal())
bearer = CustomHTTPBearer()


@admin.on_event("startup")
def create_admin():
    admin_data = validate_create(
        name="Admin",
        lastname="Marvic",
        email="example@gmail.com",
        password="administrator123"
    )
    admin_controller.create_admin(
        admin_data=admin_data[0],
        auth_data=admin_data[1]
    )
    

@admin.put("/{admin_id}", dependencies=[Depends(bearer)])
@authenticate
async def update_admin(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
    admin_data=Depends(validate_update)
) -> JSONResponse:
    result: dict = admin_controller.update_admin(
        admin_data=admin_data,
        admin_id=admin_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted 🤝",
            "message": "Updated admin ✅",
            "codes": {
                "status_code": status.HTTP_202_ACCEPTED,
            },
            "data": result
        }
    )


@admin.get("/{admin_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_admin(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_admin(admin_id=admin_id)
    )
    

@admin.get("/{admin_id}/users", dependencies=[Depends(bearer)])
@authenticate
async def get_users(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_users()
    )


@admin.get("/{admin_id}/pets", dependencies=[Depends(bearer)])
@authenticate
async def get_pets(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_pets()
    )
    

@admin.get("/{admin_id}/appointments", dependencies=[Depends(bearer)])
@authenticate
async def get_appointments(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_appointments()
    )


@admin.get("/{admin_id}/users/{user_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_user(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
    user_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_user(user_id)
    )

@admin.put("/{admin_id}/users/{user_id}", dependencies=[Depends(bearer)])
@authenticate
async def change_password_to_user(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
    new_password: Annotated[str, Body(...)],
    email: Annotated[str, Body(...)]
) -> JSONResponse:    
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "status": "Accepted 🤝",
            "message": "Updated auth for user✅",
            "codes": {
                "status_code": status.HTTP_202_ACCEPTED,
            },
            "data": admin_controller.change_password_to_user(
                new_password=new_password,
                email=email,
            )
        }
    )
    
@admin.get("/{admin_id}/pets/{pet_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_pet(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
    pet_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_pet(pet_id)
    )
    

@admin.get("/{admin_id}/appointments/{appointment_id}", dependencies=[Depends(bearer)])
@authenticate
async def get_appointment(
    request: Request,
    admin_id: Annotated[str, Path(max_length=36)],
    appointment_id: Annotated[str, Path(max_length=36)]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=admin_controller.get_appointment(appointment_id)
    )

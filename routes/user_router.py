from middlewares.user_middleware import validate_create_user_data, validate_update_user_data
from controllers.user_controller import UserControllers
from middlewares.user_middleware import Request
from fastapi import APIRouter, Depends, Path
from schemas.user_schema import User
from schemas.auth_schema import Auth
users = APIRouter()


user_controller = UserControllers()


@users.post("/", dependencies=[Depends(validate_create_user_data)])
def create_user(request: Request, user_data: User, auth_data: Auth):
    user_controller.create_user(user_data.dict(), auth_data.dict())
    return "Success"


@users.put("/{user_id}", dependencies=[Depends(validate_update_user_data)])
def update_user(request: Request, user_data: User, user_id: str = Path(...)):
    user_controller.update_user(user_data.dict(), user_id)
    return "Success"


@users.get("/{user_id}")
def update_user(request: Request, user_id: str = Path(...)):
    return user_controller.get_user(user_id)


@users.delete("/{user_id}")
def delete_user(request: Request, user_id: str = Path(...)):
    user_controller.delete_user(user_id)

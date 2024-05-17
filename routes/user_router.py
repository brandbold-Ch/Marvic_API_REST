from middlewares.user_middleware import validate_user_data
from controllers.user_controller import UserControllers
from middlewares.user_middleware import Request
from fastapi import APIRouter, Depends
from schemas.users_schema import User
from schemas.auth_schema import Auth
users = APIRouter()


user_controller = UserControllers()


@users.post("/", dependencies=[Depends(validate_user_data)])
def create_user(request: Request, user_data: User, auth_data: Auth):
    user_controller.create_user(user_data.dict(), auth_data.dict())
    return "Success"

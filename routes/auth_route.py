from controllers.auth_controller import AuthControllers
from utils.config_orm import SessionLocal
from fastapi import APIRouter, Body, Path
from typing import Annotated


auth_routes = APIRouter()
admin_controller = AuthControllers(SessionLocal())


@auth_routes.put("/change-password/{entity_id}")
async def update_auth(
        old_password: Annotated[str, Body(...)],
        new_password: Annotated[str, Body(...)],
        email: Annotated[str, Body(...)],
        entity_id: Annotated[str, Path(max_length=36)],
        role: Annotated[str, Body(...)]
) -> None:
    return admin_controller.update_auth(old_password, new_password, email, entity_id, role)

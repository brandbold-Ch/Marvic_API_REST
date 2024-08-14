import os.path

from routes.appointment_route import appointment_routes
from starlette.responses import FileResponse
from routes.user_router import user_routes
from routes.admin_route import admin
from routes.pet_router import pet_routes
from routes.auth_route import auth_routes
from fastapi import Path
from utils.config_orm import Base, engine
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from errors.exception_classes import ServerBaseException


app = FastAPI(
    title="Clínica Veterinaria Marvic (Al servicio de supermascotas) 🐕‍🦺🐈",
    description="Esta es una API para gestionar citas médicas de mascotas.",
    version="1.0.0"
)


@app.exception_handler(ServerBaseException)
async def server_base_exception_handler(request: Request, exc: ServerBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


@app.on_event("startup")
async def crete_tables():
    Base.metadata.create_all(engine)

pet_routes.include_router(appointment_routes, prefix="/{pet_id}/appointments", tags=["User Controllers"])
user_routes.include_router(pet_routes, prefix="/{user_id}/pets", tags=["User Controllers"])
app.include_router(user_routes, prefix="/api/v1/users", tags=["User Controllers"])
app.include_router(admin, prefix="/api/v1/admins", tags=["Admin Controllers"])
app.include_router(auth_routes, prefix="/api/v1/auth", tags=["Auth Controllers"])


@app.get("/image/{image_name}")
async def images(image_name=Path(max_length=41)) -> FileResponse:
    return FileResponse(f"static/images/{image_name}", media_type="image/webp")

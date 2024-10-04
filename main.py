from models.user_model import UserModel
from models.admin_model import AdminModel
from models.auth_model import AuthModel
from models.pet_model import PetModel
from models.image_model import ImageModel
from models.appointment_model import AppointmentModel
from errors.exception_classes import ServerBaseException
from routes.appointment_route import appointment_routes
from starlette.responses import FileResponse
from routes.user_router import user_routes
from routes.admin_route import admin
from routes.pet_router import pet_routes
from routes.auth_route import auth_routes
from fastapi import Path
from utils.config_orm import Base, engine
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from errors.exception_classes import FilesNotFound

app = FastAPI(
    title="Clínica Veterinaria Marvic (Al servicio de supermascotas) 🐕‍🦺🐈",
    description="Esta es una API para gestionar citas médicas de mascotas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def create_tables():
    Base.metadata.create_all(engine)


@app.exception_handler(ServerBaseException)
async def server_base_exception_handler(request: Request, exc: ServerBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


pet_routes.include_router(appointment_routes, prefix="/{pet_id}/appointments", tags=["User Controllers"])
user_routes.include_router(pet_routes, prefix="/{user_id}/pets", tags=["User Controllers"])
app.include_router(user_routes, prefix="/api/v1/users", tags=["User Controllers"])
app.include_router(admin, prefix="/api/v1/admins", tags=["Admin Controllers"])
app.include_router(auth_routes, prefix="/api/v1/auth", tags=["Auth Controllers"])


@app.get("/image/{image_name}")
async def images(image_name=Path(max_length=41)) -> FileResponse:
    try:
        return FileResponse(f"static/images/{image_name}", media_type="image/webp")
    except:
        raise FilesNotFound()


@app.get("/")
async def hello_world():
    return JSONResponse(
        status_code=200, content={
            "status": status.HTTP_200_OK,
            "message": "Bienvenido a la API de la Clínica Veterinaria Marvic 🏥",
            "detail":  {
                "Dirección": "Santos Degollado, Revolución &, Francisco Villa, 30740 Tapachula de Córdova y Ordóñez, Chis.",
                "Teléfono": "962 243 0394"
            },
            "codes": {
                "status_code": status.HTTP_200_OK,
            }
        }
    )

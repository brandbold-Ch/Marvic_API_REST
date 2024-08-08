from routes.appointment_route import appointments
from starlette.responses import FileResponse, JSONResponse
from utils.image_tools import delete_image
from routes.user_router import users
from fastapi import Path
from routes.pet_router import pets
from fastapi import FastAPI


app = FastAPI(
    title="Clínica Veterinaria Marvic (Al servicio de supermascotas) 🐕‍🦺🐈",
    description="Esta es una API para gestionar citas médicas de mascotas.",
    version="1.0.0"
)

pets.include_router(appointments, prefix="/{pet_id}/appointments", tags=["User Controllers"])
users.include_router(pets, prefix="/{user_id}/pets", tags=["User Controllers"])
app.include_router(users, prefix="/users", tags=["User Controllers"])


@app.get("/image/{image_name}")
async def images(image_name=Path(max_length=41)) -> FileResponse:
    return FileResponse(f"static/images/{image_name}", media_type="image/webp")

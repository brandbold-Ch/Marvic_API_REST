from routes.appointment_route import appointments
from starlette.responses import FileResponse
from routes.user_router import users
from routes.pet_router import pets
from fastapi import FastAPI


app = FastAPI()

pets.include_router(appointments, prefix="/{pet_id}/appointments", tags=["User Controllers"])
users.include_router(pets, prefix="/{user_id}/pets", tags=["User Controllers"])
app.include_router(users, prefix="/users", tags=["User Controllers"])

@app.get("/image/{image_name}")
async def images(image_name: str):
    """
    Endpoint para obtener una imagen específica de la carpeta estática.

    Args:
        image_name (str): Nombre del archivo de imagen.

    Returns:
        FileResponse: Archivo de imagen con el tipo de media 'image/webp'.
    """
    return FileResponse(f"static/images/{image_name}", media_type="image/webp")

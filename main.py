from starlette.responses import FileResponse
from routes.quote_route import quotes
from routes.user_router import users
from routes.pet_router import pets
from fastapi import FastAPI


app = FastAPI()


pets.include_router(quotes, prefix="/{pet_id}/quotes", tags=["User Controllers"])
users.include_router(pets, prefix="/{user_id}/pets", tags=["User Controllers"])
app.include_router(users, prefix="/users", tags=["User Controllers"])

@app.get("/image/{image_name}")
async def images(image_name: str):
    return FileResponse(f"static/images/{image_name}", media_type="image/webp")

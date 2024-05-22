from routes.user_router import users
from routes.pet_router import pets
from routes.quote_route import quotes
from fastapi import FastAPI

app = FastAPI()

pets.include_router(quotes, prefix="/{pet_id}/quotes", tags=["User Controllers"])
users.include_router(pets, prefix="/{user_id}/pets", tags=["User Controllers"])

app.include_router(users, prefix="/users", tags=["User Controllers"])

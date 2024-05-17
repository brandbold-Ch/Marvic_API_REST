from routes.user_router import users
from fastapi import FastAPI

app = FastAPI()


app.include_router(users, prefix="/users", tags=["Users Controllers"])

from fastapi import FastAPI
from schemas.users_schema import User

app = FastAPI()


@app.post("/", tags=["User"])
def set_user(user: User):
    print(user)
    return "hola"

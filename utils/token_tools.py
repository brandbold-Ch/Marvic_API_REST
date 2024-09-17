from errors.exception_classes import ExpiredTokenError, InvalidTokenError, NotFoundTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Request
import os


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        self.auto_error = False
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials is None:
            raise NotFoundTokenError()

        request.state.token = credentials.credentials
        return credentials


def create_token(payload_data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    payload_data.update({"exp": expire})

    return jwt.encode(
        payload_data,
        os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )


def verify_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )
        return decoded_token
    except JWTError as e:
        if str(e) == "Signature has expired.":
            raise ExpiredTokenError("Token has expired 💨") from e
        else:
            raise InvalidTokenError() from e

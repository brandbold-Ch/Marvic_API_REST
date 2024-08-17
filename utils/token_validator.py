from errors.exception_classes import ExpiredToken, InvalidToken
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
import os


load_dotenv()


def create_token(payload_data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=2)
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
            raise ExpiredToken("Token has expired 💨") from e
        else:
            raise InvalidToken() from e

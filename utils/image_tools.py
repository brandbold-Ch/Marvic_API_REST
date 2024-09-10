from fastapi import UploadFile
from io import BytesIO
from uuid import uuid4
from PIL import Image
import os
from errors.exception_classes import (
    InvalidImageTypeError,
    FilesNotFound,
    ServerUnknownError
)


async def upload_image(image_data: UploadFile) -> str:
    try:
        print(image_data)
        buffer = await image_data.read()
        image_stream = BytesIO(buffer)
        new_name = str(uuid4())

        with Image.open(image_stream) as image:
            webp_stream = BytesIO()
            image.save(webp_stream, format="WEBP")
            webp_stream.seek(0)
            
            with open(f"static/images/{new_name}.webp", "wb") as webp_file:
                webp_file.write(webp_stream.read())

        return f"{new_name}.webp"

    except FileNotFoundError as e:
        raise FilesNotFound(detail=e) from e

    except IOError as e:
        raise InvalidImageTypeError(detail=e) from e

    except Exception as e:
        raise ServerUnknownError(detail=e) from e


def delete_image(image_path: str) -> None:
    try:
        os.remove(f"static/images/{image_path}")

    except FileNotFoundError as e:
        raise FilesNotFound(detail=e) from e

    except Exception as e:
        raise ServerUnknownError(detail=e) from e

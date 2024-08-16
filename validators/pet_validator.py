from errors.exception_classes import ErrorInFields
from pydantic import ValidationError
from schemas.pet_schema import Pet
from typing import Annotated
from fastapi import Form, UploadFile, File


def validate_data(
        specie: Annotated[str, Form(...)],
        gender: Annotated[str, Form(...)],
        name: Annotated[str, Form(...)] = None,
        size: Annotated[str, Form(...)] = None,
        age: Annotated[str, Form(...)] = None,
        breed: Annotated[str, Form(...)] = None,
        weight: Annotated[float, Form(...)] = None,
        image: Annotated[UploadFile, File()] = None
) -> dict:
    try:
        return Pet(
            specie=specie,
            gender=gender,
            name=name,
            size=size,
            age=age,
            breed=breed,
            weight=weight,
            image=image
        ).model_dump()

    except ValidationError as e:
        raise ErrorInFields(e) from e

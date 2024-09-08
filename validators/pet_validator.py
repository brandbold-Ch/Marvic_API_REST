from errors.exception_classes import DataValidationError
from pydantic import ValidationError
from schemas.pet_schema import PetSchema
from typing import Annotated
from fastapi import Form, UploadFile, File


def validate_data(
        specie: Annotated[str, Form(...)],
        gender: Annotated[str, Form(...)],
        name: Annotated[str, Form(...)] = None,
        size: Annotated[str, Form(...)] = None,
        age: Annotated[str, Form(...)] = None,
        breed: Annotated[str, Form(...)] = None,
        weight: Annotated[str, Form(...)] = 0.0,
        image: Annotated[UploadFile, File()] = None
) -> dict:
    try:
        return PetSchema(
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
        raise DataValidationError(e) from e

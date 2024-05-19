from pydantic import BaseModel, field_validator, Field
from typing import Annotated


specie_choices: list = ["Gato", "Perro", "Otro"]
gender_choices: list = ["Macho", "Hembra"]
size_choices: list = ["Grande", "Pequeño", "Mediano"]


class Pet(BaseModel):
    name: str = Annotated[None, Field(max_length=30)]
    specie: str
    gender: str
    size: str = None
    age: str = None
    breed: str = None
    weight: float = None

    @field_validator("specie", mode="after")
    def specie_validator(cls, specie: str):
        if specie in specie_choices:
            return specie
        raise ValueError(f"Must be one of the following values {specie_choices}")

    @field_validator("gender", mode="after")
    def gender_validator(cls, gender: str):
        if gender in gender_choices:
            return gender
        raise ValueError(f"Must be one of the following values {gender_choices}")

    @field_validator("size", mode="after")
    def size_validator(cls, size: str):
        if size in size_choices:
            return size
        raise ValueError(f"Must be one of the following values {size_choices}")

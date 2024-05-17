from pydantic import BaseModel, field_validator, Field
from typing import Annotated


specie_choices: list = ["Gato", "Perro", "Otro"]
gender_choices: list = ["Macho", "Hembra"]


class Pet(BaseModel):
    name: str = Annotated[None, Field(max_length=30)]
    specie: str
    gender: str
    size: str = None
    age: str = None
    breed: str = None
    weight: float = None
    live: bool = Field(default=True)

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

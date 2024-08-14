from pydantic import BaseModel, field_validator, Field
from typing import Optional, Union
from fastapi import UploadFile
from uuid import uuid4, UUID

specie_choices: list = ["Gato", "Perro", "Otro"]
gender_choices: list = ["Macho", "Hembra"]
size_choices: list = ["Grande", "Chico", "Mediano"]


class Pet(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: Optional[str] = Field(max_length=25, default=None)
    specie: str
    gender: str
    size: Optional[str] = None
    age: Optional[str] = None
    breed: Optional[str] = None
    weight: Union[Optional[float], Optional[str]] = None
    image: Union[Optional[str], Optional[UploadFile]] = None

    class Config:
        from_attributes = True

    @field_validator("specie", mode="after")
    def specie_validator(cls, specie: str):
        if specie in specie_choices:
            return specie
        if specie == "" or specie is None:
            return None
        raise ValueError(f"Must be one of the following values {specie_choices}")

    @field_validator("gender", mode="after")
    def gender_validator(cls, gender: str):
        if gender in gender_choices:
            return gender
        if gender == "" or gender is None:
            return None
        raise ValueError(f"Must be one of the following values {gender_choices}")

    @field_validator("size", mode="after")
    def size_validator(cls, size: str):
        if size in size_choices:
            return size
        if size == "" or size is None:
            return None
        raise ValueError(f"Must be one of the following values {size_choices}")

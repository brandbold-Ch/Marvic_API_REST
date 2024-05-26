from pydantic import BaseModel, field_validator, Field
from uuid import uuid4, UUID
from fastapi import UploadFile
from typing import Optional, Union


specie_choices: list = ["Gato", "Perro", "Otro"]
gender_choices: list = ["Macho", "Hembra"]
size_choices: list = ["Grande", "Pequeño", "Mediano"]


class Pet(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: Optional[str] = Field(max_length=25, default=None)
    specie: str
    gender: str
    size: Optional[str] = None
    age: Optional[str] = None
    breed: Optional[str] = None
    weight: Union[Optional[float], Optional[str]] = None
    is_live: Optional[bool] = Field(default=True)
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

    @field_validator("age", mode="after")
    def age_validator(cls, age: str):
        if age == "":
            return None
        return age

    @field_validator("breed", mode="after")
    def breed_validator(cls, breed: str):
        if breed == "":
            return None
        return breed

    @field_validator("weight", mode="after")
    def weight_validator(cls, weight: str):
        if weight == "":
            return None
        return weight

    @field_validator("is_live", mode="after")
    def is_live_validator(cls, is_live: str):
        if is_live == "":
            return None
        return is_live

    @field_validator("image", mode="after")
    def image_validator(cls, image: UploadFile):
        if image == "":
            return None
        return image
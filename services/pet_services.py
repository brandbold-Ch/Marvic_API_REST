from decorators.validator_decorators import entity_validator
from utils.image_tools import upload_image, delete_image
from sqlalchemy.orm.session import Session
from models.image_model import ImageModel
from models.pet_model import PetModel
from uuid import uuid4


class PetServices:

    def __init__(self, session: Session) -> None:
        self.session = session

    @entity_validator(user=True)
    async def create_pet(self, **kwargs) -> dict:
        pet_data = kwargs.get("pet_data")
        image_data = pet_data.pop("image")

        pet_create = PetModel(
            **pet_data, user_id=kwargs.get("user_id")
        )
        self.session.add(pet_create)
        self.session.commit()

        if image_data is not None:
            image_path = await upload_image(image_data)
            self.session.add(ImageModel(id=uuid4(), image=image_path, pet_id=pet_create.id))
            self.session.commit()

        return pet_create.to_dict()

    @entity_validator(user=True)
    def get_pets(self, **kwargs) -> list[dict]:
        pets: list[PetModel] = kwargs.get("object_result").pets
        return [pet.to_dict() for pet in pets]

    @entity_validator(pet=True)
    def get_pet(self, **kwargs) -> dict:
        pet_data: PetModel = kwargs.get("object_result")
        return pet_data.to_dict()

    @entity_validator(pet=True)
    async def update_pet(self, **kwargs) -> dict:
        pet_update: PetModel = kwargs.get("object_result")
        pet_data = kwargs.get("pet_data")
        image_data = pet_data.pop("image")
        del pet_data["id"]

        pet_update.update_fields(**pet_data)
        self.session.add(pet_update)
        self.session.commit()

        if image_data is not None and pet_update.get_image() is None:
            image_path = await upload_image(image_data)
            self.session.add(ImageModel(id=uuid4(), image=image_path, pet_id=pet_update.id))
            self.session.commit()

        return pet_update.to_dict()

    @entity_validator(pet=True)
    def delete_pet(self, **kwargs) -> None:
        pet_delete: PetModel = kwargs.get("object_result")
        self.session.delete(pet_delete)
        self.session.commit()

        if pet_delete.get_image() is not None:
            image = pet_delete.get_image().split("/")
            delete_image(image[-1])

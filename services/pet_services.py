from decorators.error_decorators import exceptions_handler
from utils.image_tools import upload_image, delete_image
from sqlalchemy.orm.session import Session
from models.image_model import ImageModel
from models.pet_model import PetModel
from sqlalchemy import and_
from uuid import uuid4


class PetServices:

    def __init__(self, session: Session) -> None:
        self.session = session

    @exceptions_handler(verify_user=True)
    async def create_pet(self, user_id: str, pet_data: dict) -> dict:
        image_data = pet_data.pop("image")

        pet_create = PetModel(**pet_data, user_id=user_id)
        self.session.add(pet_create)
        self.session.commit()

        if image_data is not None:
            image_path = await upload_image(image_data)
            self.session.add(ImageModel(id=uuid4(), image=image_path, pet_id=pet_create.id))
            self.session.commit()

        return pet_create.to_dict()

    @exceptions_handler(verify_user=True)
    def get_pets(self, user_id: str) -> list[dict]:
        pets = (self.session.query(PetModel).where(
            user_id == PetModel.user_id
        ).all())

        return [pet.to_dict() for pet in pets]

    @exceptions_handler(verify_pet=True)
    def get_pet(self, user_id: str, pet_id: str) -> dict:
        pet_data: PetModel | None = self.session.query(PetModel).filter(
            and_(*[PetModel.user_id == user_id, PetModel.id == pet_id])
        ).first()

        return pet_data.to_dict()

    @exceptions_handler(verify_pet=True)
    async def update_pet(self, user_id: str, pet_id: str, pet_data: dict) -> dict:
        del pet_data["id"]
        image_data = pet_data.pop("image")

        pet_update: PetModel | None = self.session.query(PetModel).where(and_(*[
            PetModel.user_id == user_id,
            PetModel.id == pet_id
        ])).first()
        pet_update.update_fields(**pet_data)

        self.session.add(pet_update)
        self.session.commit()

        if image_data is not None and pet_update.get_image() is None:
            image_path = await upload_image(image_data)
            self.session.add(ImageModel(id=uuid4(), image=image_path, pet_id=pet_update.id))
            self.session.commit()

        return pet_update.to_dict()

    @exceptions_handler(verify_pet=True)
    def delete_pet(self, user_id: str, pet_id: str) -> None:
        pet_delete: PetModel | None = self.session.query(PetModel).where(and_(*[
            PetModel.user_id == user_id,
            PetModel.id == pet_id
        ])).first()
        self.session.delete(pet_delete)
        self.session.commit()

        if pet_delete.get_image() is not None:
            image = pet_delete.get_image().split("/")
            delete_image(image[-1])

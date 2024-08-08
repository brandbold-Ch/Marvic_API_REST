from decorators.entity_decorators import check_user, check_pet_context
from decorators.error_decorators import exceptions_handler
from utils.image_tools import upload_image, delete_image
from sqlalchemy.orm.session import Session
from models.image_model import ImageModel
from utils.config_orm import Base, engine
from models.pet_model import PetModel
from sqlalchemy import and_
from uuid import uuid4


class PetServices:

    def __init__(self, session: Session) -> None:
        Base.metadata.create_all(engine)
        self.session = session

    @check_user
    @exceptions_handler
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

    @check_user
    @exceptions_handler
    async def get_pets(self, user_id: str) -> list[dict]:
        pets = (self.session.query(PetModel).where(
            user_id == PetModel.user_id
        ).all())

        return [pet.to_dict() for pet in pets]

    @check_user
    @check_pet_context
    @exceptions_handler
    async def get_pet(self, user_id: str, pet_id: str) -> dict:
        pet_data: PetModel | None = self.session.query(PetModel).filter(
            and_(*[PetModel.user_id == user_id, PetModel.id == pet_id])
        ).first()

        return pet_data.to_dict()

    @check_user
    @check_pet_context
    @exceptions_handler
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

    @check_user
    @check_pet_context
    @exceptions_handler
    async def delete_pet(self, user_id: str, pet_id: str) -> None:
        pet_delete: PetModel | None = self.session.query(PetModel).where(and_(*[
            PetModel.user_id == user_id,
            PetModel.id == pet_id
        ])).first()
        self.session.delete(pet_delete)
        self.session.commit()

        if pet_delete.get_image() is not None:
            delete_image(pet_delete.get_image())

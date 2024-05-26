from errors.exception_classes import DoesNotExistInDatabase, InvalidUUID
from sqlalchemy.exc import DataError, SQLAlchemyError
from utils.config_orm import Base, engine, Session
from services.mw_services import MWServices
from sqlalchemy.sql import update, delete
from models.pet_model import PetModel
from utils.image_tools import upload_image, delete_image
from models.image_model import ImageModel
from sqlalchemy import and_
from uuid import uuid4


class PetServices:

    def __init__(self) -> None:
        Base.metadata.create_all(engine)
        self.session = Session()
        self.mw = MWServices()

    async def create_pet(self, user_id: str, pet_data: dict) -> None:
        success: bool = False
        image_path: str = None
        try:
            self.mw.get_user(user_id)
            pet_data["user_id"] = user_id
            image_data = pet_data.pop("image")
                        
            if image_data is not None:
                image_path = await upload_image(image_data)
                self.session.add(ImageModel(id=uuid4(), image=image_path, pet_id=pet_data["id"]))

            self.session.add(PetModel(**pet_data))
            self.session.commit()
            success = True

        except DataError:
            self.session.rollback()
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query ⚠️")
  
        finally:
            if success is False and image_path is not None:
                await delete_image(image_path)
                
            self.session.close()          

    async def get_pets(self, user_id: str) -> list[dict]:
        try:
            self.mw.get_user(user_id)
            pets_list: list = []

            pets = (self.session.query(PetModel).filter(and_(*[
                PetModel.user_id == user_id
            ])).all())
            
            for pet in pets:
                image = self.session.query(ImageModel).filter(
                    and_(*[ImageModel.pet_id == pet.id])
                ).first()
                
                if image:
                    pets_list.append(pet.to_representation(image.image))
                else:
                    pets_list.append(pet.to_representation())

            return pets_list

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError as err:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    async def get_pet(self, user_id: str, pet_id: str) -> dict:
        try:
            self.mw.get_user(user_id)

            pet_data = self.session.query(PetModel).filter(
                and_(*[PetModel.user_id == user_id, PetModel.id == pet_id])
            ).first()
            image_data = self.session.query(ImageModel).filter(
                and_(*[ImageModel.pet_id == pet_id])
            ).first()

            if pet_data:
                if image_data:
                    return pet_data.to_representation(image_data.image)
                return pet_data.to_representation()
            else:
                raise DoesNotExistInDatabase("The pet does not exist ❌")

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    async def update_pet(self, user_id: str, pet_id: str, pet_data: dict) -> None:
        try:
            self.get_pet(user_id, pet_id)
            del pet_data["id"]

            stmt = (update(PetModel)
                    .where(and_(*[PetModel.user_id == user_id, PetModel.id == pet_id]))
                    .values(**pet_data))
            self.session.execute(stmt)
            self.session.commit()

        except DataError:
            self.session.rollback()
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query")

        finally:
            self.session.close()

    async def delete_pet(self, user_id: str, pet_id: str) -> None:
        try:
            self.get_pet(user_id, pet_id)

            stmt = delete(PetModel).where(and_(*[
                PetModel.user_id == user_id,
                PetModel.id == pet_id
            ]))
            self.session.execute(stmt)
            self.session.commit()

        except DataError:
            self.session.rollback()
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

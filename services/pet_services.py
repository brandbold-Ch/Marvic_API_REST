from sqlalchemy.exc import DataError, SQLAlchemyError
from utils.config_orm import Base, engine, Session
from services.mw_services import MWServices
from sqlalchemy.sql import update, delete
from models.pet_model import PetModel
from utils.image_tools import upload_image, delete_image
from models.image_model import ImageModel
from sqlalchemy import and_
from uuid import uuid4
from errors.handler_exceptions import (
    handle_data_error, 
    handle_sqlalchemy_error,
    handle_do_not_exists
)


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
            handle_data_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()
  
        finally:
            if success is False and image_path is not None:
                await delete_image(image_path)
            self.session.close()          

    async def get_pets(self, user_id: str) -> list[dict]:
        try:
            self.mw.get_user(user_id)

            pets = (self.session.query(PetModel).filter(and_(*[
                PetModel.user_id == user_id
            ])).all())
            
            return [pet.to_dict() for pet in pets]

        except DataError:
            handle_data_error()

        except SQLAlchemyError as err:
            print(err)
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    async def get_pet(self, user_id: str, pet_id: str) -> dict:
        try:
            self.mw.get_user(user_id)

            pet_data = self.session.query(PetModel).filter(
                and_(*[PetModel.user_id == user_id, PetModel.id == pet_id])
            ).first()

            if pet_data:
                return pet_data.to_dict()
            else:
                handle_do_not_exists("pet")

        except DataError:
            handle_data_error()

        except SQLAlchemyError:
            handle_sqlalchemy_error()

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
            handle_data_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

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
            handle_data_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

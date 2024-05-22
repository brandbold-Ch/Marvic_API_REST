from errors.exception_classes import DoesNotExistInDatabase, InvalidUUID
from sqlalchemy.exc import DataError, SQLAlchemyError
from utils.config_orm import Base, engine, Session
from services.mw_services import MWServices
from sqlalchemy.sql import update, delete
from models.pet_model import PetModel
from sqlalchemy import and_


class PetServices:

    def __init__(self) -> None:
        Base.metadata.create_all(engine)
        self.session = Session()
        self.mw = MWServices()

    def create_pet(self, user_id: str, pet_data: dict) -> None:
        try:
            self.mw.get_user(user_id)
            pet_data["user_id"] = user_id

            self.session.add(PetModel(**pet_data))
            self.session.commit()

        except DataError:
            self.session.rollback()
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def get_pets(self, user_id: str) -> list[dict]:
        try:
            self.mw.get_user(user_id)

            pets = (self.session.query(PetModel).filter(and_(*[
                PetModel.user_id == user_id
            ])).all())

            return [pet.to_representation() for pet in pets]

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def get_pet(self, user_id: str, pet_id: str) -> dict:
        try:
            self.mw.get_user(user_id)

            pet_data = self.session.query(PetModel).filter(
                and_(*[PetModel.user_id == user_id, PetModel.id == pet_id])
            ).first()

            if pet_data is None:
                raise DoesNotExistInDatabase("The pet does not exist ❌")
            return pet_data.to_representation()

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def update_pet(self, user_id: str, pet_id: str, pet_data: dict) -> None:
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
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def delete_pet(self, user_id: str, pet_id: str) -> None:
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

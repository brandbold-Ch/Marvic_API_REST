from errors.exception_classes import DoesNotExistInDatabase, InvalidUUID
from utils.config_orm import Base, engine, Session
from services.mw_services import MWServices
from sqlalchemy.exc import SQLAlchemyError
from models.quote_model import QuoteModel
from models.user_model import UserModel
from models.pet_model import PetModel
from sqlalchemy.exc import DataError
from sqlalchemy.sql import delete
from sqlalchemy import and_


class QuoteServices:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.mw = MWServices()

    def create_quote(self, user_id: str, pet_id: str, quote_data: dict) -> None:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)
            quote_data["user_id"] = user_id
            quote_data["pet_id"] = pet_id

            self.session.add(QuoteModel(**quote_data))
            self.session.commit()

        except DataError:
            self.session.rollback()
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def get_quote(self, user_id: str, quote_id: str, pet_id: str) -> dict:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)

            quote_data = self.session.query(QuoteModel).filter(and_(*[
                UserModel.id == user_id,
                QuoteModel.id == quote_id,
                PetModel.id == pet_id
            ])).first()

            if quote_data is None:
                raise DoesNotExistInDatabase("The record does not exist ❌")
            return quote_data.to_representation()

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def get_quotes(self, user_id: str, pet_id: str) -> list[dict]:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)

            quotes = (self.session.query(QuoteModel).filter(and_(*[
                UserModel.id == user_id, PetModel.id == pet_id
            ])).all())
            return [quote.to_representation() for quote in quotes]

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def delete_quotes(self, user_id: str, quote_id: str, pet_id: str) -> None:
        try:
            self.get_quote(user_id, quote_id, pet_id)

            stmt = delete(QuoteModel).where(and_(*[
                UserModel.id == user_id,
                QuoteModel.id == quote_id,
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

from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.sql.expression import update, delete
from utils.config_orm import Base, engine, Session
from models.user_model import UserModel
from models.auth_model import AuthModel
from models.pet_model import PetModel
from sqlalchemy import and_
from errors.handler_exceptions import (
    handle_data_error, 
    handle_sqlalchemy_error, 
    handle_integrity_error, 
    handle_do_not_exists
)


class UserServices:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def create_user(self, user_data: dict, auth_data: dict) -> None:
        try:
            auth_data["user_id"] = user_data["id"]

            self.session.add(UserModel(**user_data))
            self.session.add(AuthModel(**auth_data))
            self.session.commit()

        except IntegrityError:
            self.session.rollback()
            handle_integrity_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def update_user(self, user_data: dict, user_id: str) -> None:
        try:
            self.get_user(user_id)
            del user_data["id"]

            stmt = (update(UserModel)
                    .where(and_(*[UserModel.id == user_id]))
                    .values(**user_data))
            self.session.execute(stmt)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def get_user(self, user_id: str) -> dict:
        try:
            user_data = self.session.query(UserModel).get(user_id)

            if user_data is None:
                handle_do_not_exists("user")
            return user_data.to_dict()

        except DataError:
            handle_data_error()

        except SQLAlchemyError:
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def delete_user(self, user_id: str) -> None:
        try:
            self.get_user(user_id)

            stmt_auth = delete(AuthModel).where(and_(*[AuthModel.user_id == user_id]))
            stmt_user = delete(UserModel).where(and_(*[UserModel.id == user_id]))
            stmt_pets = delete(PetModel).where(and_(*[PetModel.user_id == user_id]))

            self.session.execute(stmt_auth)
            self.session.execute(stmt_user)
            self.session.execute(stmt_pets)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.sql.expression import update, delete
from utils.config_orm import Base, engine, Session
from models.user_model import UserModel
from models.auth_model import AuthModel
from models.pet_model import PetModel
from sqlalchemy.orm import session
from sqlalchemy import and_
from errors.handler_exceptions import (
    handle_sqlalchemy_error, 
    handle_integrity_error, 
    handle_do_not_exists,
    handle_data_error
)


class UserServices:

    def __init__(self) -> None:
        Base.metadata.create_all(engine)
        self.session: session.Session = Session()

    def create_user(self, user_data: dict, auth_data: dict) -> dict[dict, dict]:
        try:
            auth_data["user_id"] = user_data["id"]
            print(auth_data["user_id"])
            print(user_data["id"])

            user = UserModel(**user_data)
            auth = AuthModel(**auth_data)

            self.session.add(user)
            self.session.add(auth)
            self.session.commit()

            return {
                "user_data": user.to_dict(), 
                "auth_data": auth.to_dict()
            }

        except IntegrityError:
            self.session.rollback()
            handle_integrity_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def update_user(self, user_data: dict, user_id: str) -> dict:
        try:
            del user_data["id"]

            stmt = (
                update(UserModel)
                .where(and_(*[UserModel.id == user_id]))
                .values(**user_data)
                .returning(UserModel.id)
            )
            
            update_result = self.session.execute(stmt)
            self.session.commit()

            if update_result.fetchone() is None:
                handle_do_not_exists("user")
            return self.get_user(user_id)

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def get_user(self, user_id: str) -> dict:
        try:
            user_data: UserModel = self.session.get(UserModel, user_id)

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
            stmt_pets = delete(PetModel).where(and_(*[PetModel.user_id == user_id]))
            self.session.execute(stmt_pets)
            self.session.commit()

            stmt_auth = delete(AuthModel).where(and_(*[AuthModel.user_id == user_id]))
            self.session.execute(stmt_auth)
            self.session.commit()

            stmt_user = (
                delete(UserModel)
                .where(and_(*[UserModel.id == user_id]))
                .returning(UserModel.id)
            )
            delete_result = self.session.execute(stmt_user)
            self.session.commit()

            if delete_result.fetchone() is None:
                handle_do_not_exists("user")

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

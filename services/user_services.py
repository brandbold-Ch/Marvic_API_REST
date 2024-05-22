from errors.exception_classes import DuplicatedInDatabase, DoesNotExistInDatabase, InvalidUUID
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.sql.expression import update, delete
from utils.config_orm import Base, engine, Session
from models.user_model import UserModel
from models.auth_model import AuthModel
from sqlalchemy import and_


class UserServices:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def create_user(self, user_data: dict, auth_data: dict) -> None:
        try:
            user = UserModel(**user_data)
            auth = AuthModel(**auth_data, user_id=user.id)

            self.session.add(user)
            self.session.add(auth)
            self.session.commit()

        except IntegrityError:
            self.session.rollback()
            raise DuplicatedInDatabase("That account already exists")

        except SQLAlchemyError:
            self.session.rollback()
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def update_user(self, user_data: dict, user_id: str) -> None:
        try:
            self.get_user(user_id)
            del user_data["id"]

            stmt = update(UserModel).where(and_(*[UserModel.id == user_id])).values(**user_data)
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

    def get_user(self, user_id: str) -> dict:
        try:
            user_data = self.session.query(UserModel).get(user_id)

            if user_data is None:
                raise DoesNotExistInDatabase("The user does not exist ❌")
            return user_data.to_representation()

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

        except SQLAlchemyError:
            raise Exception("There was a conflict in the database query ⚠️")

        finally:
            self.session.close()

    def delete_user(self, user_id: str) -> None:
        try:
            self.get_user(user_id)

            stmt = delete(UserModel).where(and_(*[UserModel.id == user_id]))
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

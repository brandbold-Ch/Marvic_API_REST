from errors.exception_classes import DuplicatedInDatabase, DoesNotExistInDatabase, InvalidUUID
from sqlalchemy.sql.expression import update, delete
from utils.config_orm import Base, engine, Session
from sqlalchemy.exc import IntegrityError, DataError
from models.user_model import User
from models.auth_model import Auth


class UserServices:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def create_user(self, user_data: dict, auth_data: dict) -> None:
        try:
            user = User(**user_data)
            auth = Auth(**auth_data, user_id=user.id)

            self.session.add(user)
            self.session.add(auth)
            self.session.commit()

        except IntegrityError as error:
            self.session.rollback()
            raise DuplicatedInDatabase(error)

        finally:
            self.session.close()

    def update_user(self, user_data: dict, user_id: str) -> None:
        try:
            self.get_user(user_id)
            del user_data["id"]

            stmt = update(User).where(User.id == user_id).values(**user_data)
            self.session.execute(stmt)
            self.session.commit()

        except DataError as error:
            self.session.rollback()
            raise InvalidUUID(error)

        finally:
            self.session.close()

    def get_user(self, user_id: str) -> User:
        try:
            user = self.session.query(User).get(user_id)

            if user:
                return user
            raise DoesNotExistInDatabase("The entity does not exist")

        except DataError as error:
            raise InvalidUUID(error)

        finally:
            self.session.close()

    def delete_user(self, user_id: str) -> None:
        try:
            self.get_user(user_id)

            stmt = delete(User).where(User.id == user_id)
            self.session.execute(stmt)
            self.session.commit()

        except DataError as error:
            raise InvalidUUID(error)

        finally:
            self.session.close()

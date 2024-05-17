from sqlalchemy.sql.expression import update, delete
from utils.config_orm import Base, engine, Session
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

        except:
            self.session.rollback()
        finally:
            self.session.close()

    def update_user(self, user_data: dict, user_id: str) -> None:
        try:
            del user_data["id"]

            stmt = update(User).where(User.id == user_id).values(**user_data)
            self.session.execute(stmt)
            self.session.commit()

        except:
            self.session.rollback()
        finally:
            self.session.close()

    def get_user(self, user_id: str) -> User:
        try:
            return self.session.query(User).get(user_id)

        except:
            ...
        finally:
            self.session.close()

    def delete_user(self, user_id: str) -> None:
        try:
            stmt = delete(User).where(User.id == user_id)
            self.session.execute(stmt)
            self.session.commit()

        except:
            self.session.rollback()

        finally:
            self.session.close()

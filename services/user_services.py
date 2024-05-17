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

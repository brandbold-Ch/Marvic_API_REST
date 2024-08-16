from services.user_services import UserServices
from sqlalchemy.orm import Session


class UserControllers:

    def __init__(self, session: Session) -> None:
        self.user = UserServices(session)

    def create_user(self, **kwargs) -> dict[dict, dict]:
        return self.user.create_user(**kwargs)

    def update_user(self, **kwargs) -> dict:
        return self.user.update_user(**kwargs)

    def get_user(self, **kwargs) -> dict:
        return self.user.get_user(**kwargs)

    def delete_user(self, **kwargs) -> None:
        self.user.delete_user(**kwargs)

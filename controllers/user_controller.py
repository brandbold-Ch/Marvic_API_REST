from services.user_services import UserServices
from sqlalchemy.orm import Session


class UserControllers:

    def __init__(self, session: Session) -> None:
        self.user = UserServices(session)

    def create_user(self, user_data: dict, auth_data: dict) -> dict[dict, dict]:
        return self.user.create_user(user_data, auth_data)

    def update_user(self, user_data: dict, user_id: str) -> dict:
        return self.user.update_user(user_data, user_id)

    def get_user(self, user_id: str) -> dict:
        return self.user.get_user(user_id)

    def delete_user(self, user_id: str) -> None:
        self.user.delete_user(user_id)

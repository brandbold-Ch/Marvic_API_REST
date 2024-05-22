from services.user_services import UserServices


class UserControllers:

    def __init__(self) -> None:
        self.user = UserServices()

    def create_user(self, user_data: dict, auth_data: dict) -> None:
        self.user.create_user(user_data, auth_data)

    def update_user(self, user_data: dict, user_id: str) -> None:
        self.user.update_user(user_data, user_id)

    def get_user(self, user_id: str) -> dict:
        return self.user.get_user(user_id)

    def delete_user(self, user_id: str) -> None:
        self.user.delete_user(user_id)

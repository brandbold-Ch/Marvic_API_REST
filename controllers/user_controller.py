from services.user_services import UserServices


class UserControllers:

    def __init__(self) -> None:
        self.user = UserServices()

    def create_user(self, user_data: dict, auth_data: dict) -> None:
        self.user.create_user(user_data, auth_data)

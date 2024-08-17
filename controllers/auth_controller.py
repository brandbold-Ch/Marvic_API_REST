from services.auth_services import AuthServices
from sqlalchemy.orm import Session


class AuthControllers:

    def __init__(self, session: Session) -> None:
        self.auth = AuthServices(session)

    def update_auth(self, **kwargs) -> dict:
        return self.auth.update_auth(**kwargs)

    def get_auth(self, **kwargs) -> dict:
        return self.auth.get_auth(**kwargs)

    def auth_login(self, **kwargs) -> dict:
        return self.auth.auth_login(**kwargs)

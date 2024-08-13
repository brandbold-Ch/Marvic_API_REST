from services.auth_services import AuthServices
from sqlalchemy.orm import Session


class AuthControllers:

    def __init__(self, session: Session) -> None:
        self.auth = AuthServices(session)

    def update_auth(self, old_password: str, new_password: str, email: str, entity_id: str, role: str) -> dict:
        return self.auth.update_auth(old_password, new_password, email, entity_id, role)

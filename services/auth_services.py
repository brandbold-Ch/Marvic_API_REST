from utils.token_validator import create_token
from sqlalchemy.orm.session import Session
from models.auth_model import AuthModel
from schemas.auth_schema import Auth
from decorators.validator_decorators import (
    verify_passwords_for_change,
    verify_passwords_for_login,
    entity_validator
)


class AuthServices:

    def __init__(self, session: Session):
        self.session = session

    @entity_validator(auth=True)
    def get_auth(self, **kwargs) -> dict:
        return kwargs.get("object_result").to_dict()

    @verify_passwords_for_change
    def update_auth(self, **kwargs) -> dict:
        auth_update: AuthModel = kwargs.get("object_result")
        self.session.add(auth_update)
        self.session.commit()

        return auth_update.to_dict()

    def recover_password(self) -> None:
        pass

    @verify_passwords_for_login
    def auth_login(self,  **kwargs) -> dict:
        auth_data: AuthModel = kwargs.get("object_result")
        return {
            "token": create_token({
                "user_id": auth_data.user_id,
                "role": auth_data.role
            }),
            "user_id": auth_data.user_id,
            "role": auth_data.role
        }

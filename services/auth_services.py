from utils.token_tools import create_token
from sqlalchemy.orm.session import Session
from models.auth_model import AuthModel
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

    @verify_passwords_for_login
    def auth_login(self,  **kwargs) -> dict:
        auth_data: AuthModel = kwargs.get("object_result")
        ctx_id = str(auth_data.user_id) if auth_data.user_id is not None else str(auth_data.admin_id)
        
        return {
            "token": create_token({
                "user_id": ctx_id,
                "role": auth_data.role
            }),
            "user_id": ctx_id,
            "role": auth_data.role
        }

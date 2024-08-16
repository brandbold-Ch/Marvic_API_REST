from decorators.validator_decorators import entity_validator, verify_passwords, verify_auth_by_email
from sqlalchemy.orm.session import Session
from models.auth_model import AuthModel
from schemas.auth_schema import Auth


class AuthServices:

    def __init__(self, session: Session):
        self.session = session

    @entity_validator(auth=True)
    def get_auth(self, **kwargs) -> dict:
        return kwargs.get("object_result").to_dict()

    @verify_passwords
    def update_auth(self, **kwargs) -> dict:
        auth_update: AuthModel = kwargs.get("object_result")
        self.session.add(auth_update)
        self.session.commit()

        return auth_update.to_dict()

    def recover_password(self) -> None:
        pass

from errors.handler_exceptions import handle_do_not_exists
from decorators.error_decorators import validation_handler
from sqlalchemy.orm.session import Session
from models.admin_model import AdminModel
from models.auth_model import AuthModel
import bcrypt


class AuthServices:

    def __init__(self, session: Session):
        self.session = session

    def update_auth(
            self,
            old_password: str,
            new_password: str,
            email: str,
            entity_id: str,
            role: str
    ) -> dict:
        if role == "USER":
            user_auth: AuthModel | None = (
                self.session.query(AuthModel)
                .where(entity_id == AuthModel.user_id)
                .first()
            )

            if user_auth is not None:
                stored_hash: str = user_auth.password

                if bcrypt.checkpw(old_password.encode("utf-8"), stored_hash.encode("utf-8")):
                    hashed_password = bcrypt.hashpw(
                        new_password.encode("utf-8"),
                        bcrypt.gensalt(12)
                    ).decode("utf-8")

                    user_auth.update_credentials_fields(email, hashed_password)
                    self.session.add(user_auth)
                    self.session.commit()

                    return user_auth.to_dict()
                else:
                    raise Exception("Incorrect password")
            else:
                handle_do_not_exists("user")

        elif role == "ADMINISTRATOR":
            pass

        else:
            raise Exception("Not found role")

    def recover_password(self) -> None:
        pass

from decorators.error_decorators import exceptions_handler
from sqlalchemy.orm.session import Session
from utils.image_tools import delete_image
from models.user_model import UserModel
from models.auth_model import AuthModel


class UserServices:

    def __init__(self, session: Session) -> None:
        self.session = session

    @exceptions_handler()
    def create_user(self, user_data: dict, auth_data: dict) -> dict:
        user_create = UserModel(**user_data)
        auth_create = AuthModel(**auth_data, user_id=user_create.id)

        self.session.add(user_create)
        self.session.add(auth_create)
        self.session.commit()

        return user_create.to_dict()

    @exceptions_handler(verify_user=True)
    def update_user(self, user_id: str, user_data: dict) -> dict:
        del user_data["id"]

        user_update: UserModel | None = (
            self.session.query(UserModel)
            .where(user_id == UserModel.id)
            .first()
        )
        user_update.update_fields(**user_data)
        self.session.add(user_update)
        self.session.commit()

        return user_update.to_dict()

    @exceptions_handler(verify_user=True)
    def get_user(self, user_id: str) -> dict:
        user_data: UserModel | None = self.session.get(UserModel, user_id)

        return user_data.to_dict()

    @exceptions_handler(verify_user=True)
    def delete_user(self, user_id: str) -> None:
        user_delete: UserModel | None = (
            self.session.query(UserModel)
            .where(user_id == UserModel.id)
            .first()
        )
        self.session.delete(user_delete)
        self.session.commit()

        for pet in user_delete.pets:
            if pet.get_image() is not None:
                image = pet.get_image().split("/")
                delete_image(image[-1])

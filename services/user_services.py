from decorators.error_decorators import validation_handler, handle_exceptions
from sqlalchemy.orm.session import Session
from utils.image_tools import delete_image
from models.user_model import UserModel
from models.auth_model import AuthModel


class UserServices:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_exceptions
    def create_user(self, **kwargs) -> dict:
        user_data = kwargs.get("user_data")
        auth_data = kwargs.get("auth_data")

        user_create = UserModel(**user_data)
        auth_create = AuthModel(**auth_data, user_id=user_create.id)

        self.session.add(user_create)
        self.session.add(auth_create)
        self.session.commit()

        return user_create.to_dict()

    @validation_handler(user=True)
    def update_user(self, **kwargs) -> dict:
        user_update: UserModel = kwargs.get("object_result")
        user_data = kwargs.get("user_data")
        del user_data["id"]

        user_update.update_fields(**user_data)
        self.session.add(user_update)
        self.session.commit()

        return user_update.to_dict()

    @validation_handler(user=True)
    def get_user(self, **kwargs) -> dict:
        user_data: UserModel = kwargs.get("object_result")
        return user_data.to_dict()

    @validation_handler(user=True)
    def delete_user(self, **kwargs) -> None:
        user_delete: UserModel = kwargs.get("object_result")
        self.session.delete(user_delete)
        self.session.commit()

        for pet in user_delete.pets:
            if pet.get_image() is not None:
                image = pet.get_image().split("/")
                delete_image(image[-1])

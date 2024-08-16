from errors.exception_classes import DoesNotExistInDatabase, PasswordDoesNotMatch, ErrorInFields
from models.appointment_model import AppointmentModel
from .error_decorators import handle_exceptions
from models.admin_model import AdminModel
from models.user_model import UserModel
from models.auth_model import AuthModel
from models.pet_model import PetModel
from typing import Callable
import bcrypt
import re


def check_email(email: str) -> str:
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return email
    else:
        raise ErrorInFields("The email format is incorrect ✉️")


def verify_user(_obj, user_id: str) -> UserModel:
    user: UserModel = _obj.session.get(UserModel, user_id)
    if user is None:
        raise DoesNotExistInDatabase("The user does not exist 🤦‍♂️")
    return user


def verify_auth_by_email(_obj, email: str) -> AuthModel:
    auth = _obj.session.query(AuthModel).where(
        AuthModel.email == email
    ).first()
    if auth is None:
        raise DoesNotExistInDatabase("The auth does not exist 🔐")
    return auth


def verify_auth_by_id(_obj, entity_id: str, role: str) -> AuthModel:
    auth: AuthModel | None = None

    match role:
        case "USER":
            auth = _obj.session.query(AuthModel).where(
                AuthModel.user_id == entity_id
            ).first()
            if auth is None:
                raise DoesNotExistInDatabase("The auth does not exist 🔐")

        case "ADMINISTRATOR":
            auth = _obj.session.query(AuthModel).where(
                AuthModel.admin_id == entity_id
            ).first()
            if auth is None:
                raise DoesNotExistInDatabase("The auth does not exist 🔐")

        case _:
            raise ErrorInFields("The role must be USER or ADMINISTRATOR ❓")


    return auth


def verify_passwords(func: Callable) -> Callable:
    @handle_exceptions
    def wrapper(self, **kwargs):
        auth_data: AuthModel = verify_auth_by_id(
            self, kwargs.get("entity_id"),
            kwargs.get("role")
        )
        old_password: bytes = kwargs.get("old_password").encode("utf-8")
        password: bytes = auth_data.password.encode("utf-8")
        new_password: str = bcrypt.hashpw(
            kwargs.get("new_password").encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        if bcrypt.checkpw(old_password, password):
            auth_data.email = check_email(kwargs.get("email"))
            auth_data.password = new_password

            return func(
                self, **kwargs,
                object_result=auth_data,
                auth_data=auth_data
            )
        else:
            raise PasswordDoesNotMatch()
    return wrapper


def verify_admin(_obj, admin_id: str) -> AdminModel:
    admin: AdminModel = _obj.session.get(AdminModel, admin_id)
    if admin is None:
        raise DoesNotExistInDatabase("The admin does not exist 🤦️")
    return admin


def verify_pet(_obj, user_id: str, pet_id: str) -> PetModel:
    pet: PetModel = _obj.session.get(PetModel, pet_id)

    if pet is None:
        raise DoesNotExistInDatabase("The pet does not exist 🐶")
    if str(pet.user_id) != user_id:
        raise DoesNotExistInDatabase(
            "The user does not exist or is not your pet 🤦‍♂️‍🐶"
        )
    return pet


def verify_appointment(
        _obj,
        user_id: str,
        pet_id: str,
        appointment_id: str
) -> AppointmentModel:
    appointment: AppointmentModel = _obj.session.get(
        AppointmentModel,
        appointment_id
    )
    if appointment is None:
        raise DoesNotExistInDatabase("The appointment does not exist 📑")
    if str(appointment.user_id) != user_id:
        raise DoesNotExistInDatabase(
            "The user does not exist or is not related to this appointment 🤦‍♂️📑"
        )
    if str(appointment.pet_id) != pet_id:
        raise DoesNotExistInDatabase(
            "The pet does not exist or is not related to this quote 🐶📑"
        )
    return appointment


def entity_validator(
        auth: bool = False,
        user: bool = False,
        pet: bool = False,
        appointment: bool = False
) -> Callable:
    def decorator(func: Callable):
        @handle_exceptions
        def wrapper(self, **kwargs):
            if user:
                return func(
                    self, **kwargs, object_result=verify_user(self, kwargs.get("user_id"))
                )
            elif pet:
                return func(
                    self, **kwargs, object_result=verify_pet(
                        self, kwargs.get("user_id"), kwargs.get("pet_id")
                    )
                )
            elif auth:
                return func(
                    self, **kwargs, object_result=verify_auth_by_email(
                        self, kwargs.get("email")
                    )
                )
            elif appointment:
                return func(
                    self, **kwargs, object_result=verify_appointment(
                        self, kwargs.get("user_id"),
                        kwargs.get("pet_id"),
                        kwargs.get("appointment_id")
                    )
                )
            return func(self, **kwargs)
        return wrapper
    return decorator

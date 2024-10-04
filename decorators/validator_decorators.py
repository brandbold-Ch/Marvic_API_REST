from models.appointment_model import AppointmentModel
from .error_decorators import handle_exceptions
from utils.token_tools import verify_token
from models.admin_model import AdminModel
from models.user_model import UserModel
from models.auth_model import AuthModel
from models.pet_model import PetModel
from fastapi.requests import Request
from typing import Callable
from functools import wraps
import bcrypt
import re
from errors.exception_classes import (
    DbNotFoundError,
    DuplicatedAppointmentError,
    BusyAppointmentError,
    PasswordDoNotMatchError,
    DataValidationError,
    IncorrectUserError
)


def check_email(email: str) -> str:
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return email
    else:
        raise DataValidationError("The email format is incorrect ✉️")


def verify_user(_obj, user_id: str) -> UserModel:
    user: UserModel = _obj.session.get(UserModel, user_id)
    if user is None:
        raise DbNotFoundError("The user does not exist 🤦‍♂️")
    return user


def verify_auth_by_email(_obj, email: str) -> AuthModel:
    auth = _obj.session.query(AuthModel).where(
        AuthModel.email == email
    ).first()
    if auth is None:
        raise DbNotFoundError("The auth does not exist 🔐")
    return auth


def verify_auth_by_id(_obj, user_id: str, role: str) -> AuthModel:
    auth: AuthModel | None = None

    match role:
        case "USER":
            auth = _obj.session.query(AuthModel).where(
                AuthModel.user_id == user_id
            ).first()
            if auth is None:
                raise DbNotFoundError("The user does not exist 🤦‍♂️🔐")

        case "ADMINISTRATOR":
            auth = _obj.session.query(AuthModel).where(
                AuthModel.admin_id == user_id
            ).first()
            if auth is None:
                raise DbNotFoundError("The admin does not exist 🤦️🔐")

        case _:
            raise DataValidationError("The role must be USER or ADMINISTRATOR ❓")
    return auth


def appointment_checker(func: Callable) -> Callable:
    @handle_exceptions
    def wrapper(self, **kwargs):
        appt_data = kwargs.get("appointment_data")
        pet_data = kwargs.get("object_result")

        conflicting_appointments = (self.session
            .query(AppointmentModel)
            .where(AppointmentModel.expired == False)
        ).all()

        for appointment in conflicting_appointments:        
            if appointment.pet_id == pet_data.id:
                raise DuplicatedAppointmentError()
            
            if appointment.timestamp == appt_data["timestamp"]:
                raise BusyAppointmentError()

        return func(self, **kwargs)
    return wrapper


def verify_passwords_for_login(func: Callable) -> Callable:
    @handle_exceptions
    def wrapper(self, **kwargs):
        auth_data: AuthModel = verify_auth_by_email(
            self, check_email(kwargs.get("email")),
        )
        password: bytes = kwargs.get("password").encode("utf-8")
        password_db: bytes = auth_data.password.encode("utf-8")

        if bcrypt.checkpw(password, password_db):
            return func(
                self, **kwargs,
                object_result=auth_data
            )
        else:
            raise PasswordDoNotMatchError()
    return wrapper


def verify_passwords_for_change(func: Callable) -> Callable:
    @handle_exceptions
    def wrapper(self, **kwargs):
        auth_data: AuthModel = verify_auth_by_id(
            self, kwargs.get("user_id"), kwargs.get("role")
        )
        ctx_password: bytes = kwargs.get("ctx_password").encode("utf-8")
        password: bytes = auth_data.password.encode("utf-8")
        new_password: str = bcrypt.hashpw(
            kwargs.get("new_password").encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        if bcrypt.checkpw(ctx_password, password):
            auth_data.email = check_email(kwargs.get("email"))
            auth_data.password = new_password

            return func(
                self, **kwargs,
                object_result=auth_data
            )
        else:
            raise PasswordDoNotMatchError()
    return wrapper


def verify_admin(_obj, admin_id: str) -> AdminModel:
    admin: AdminModel = _obj.session.get(AdminModel, admin_id)
    if admin is None:
        raise DbNotFoundError("The admin does not exist 🤦️")
    return admin


def verify_pet(_obj, user_id: str, pet_id: str) -> PetModel:
    pet: PetModel = _obj.session.get(PetModel, pet_id)

    if pet is None:
        raise DbNotFoundError("The pet does not exist 🐶")

    if str(pet.user_id) != user_id:
        raise DbNotFoundError(
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
        raise DbNotFoundError("The appointment does not exist 📑")

    if str(appointment.user_id) != user_id:
        raise DbNotFoundError(
            "The user does not exist or is not related to this appointment 🤦‍♂️📑"
        )

    if str(appointment.pet_id) != pet_id:
        raise DbNotFoundError(
            "The pet does not exist or is not related to this quote 🐶📑"
        )
    return appointment


def entity_validator(
        auth: bool = False,
        user: bool = False,
        pet: bool = False,
        admin: bool = False,
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
                        self, kwargs.get("user_id"),
                        kwargs.get("pet_id")
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
            elif admin:
                return func(
                    self, **kwargs, object_result=verify_admin(
                        self, kwargs.get("admin_id")
                    )
                )
                
            return func(self, **kwargs)
        return wrapper
    return decorator


def authenticate(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        user_req: dict = verify_token(request.headers.get("authorization")[7:])

        match user_req["role"]:
            case "USER":
                if user_req["user_id"] == kwargs.get("user_id"):
                    return await func(*args, **kwargs)
                else:
                    raise IncorrectUserError()
            
            case "ADMINISTRATOR":
                if user_req["user_id"] == (kwargs.get("user_id") or kwargs.get("admin_id")):
                    return await func(*args, **kwargs)
                else:
                    raise IncorrectUserError()
    return wrapper
 
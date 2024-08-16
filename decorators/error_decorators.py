from errors.exception_classes import InvalidId, DuplicatedInDatabase, UnknownError
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from errors.exception_classes import DoesNotExistInDatabase
from models.appointment_model import AppointmentModel
from models.admin_model import AdminModel
from models.user_model import UserModel
from models.pet_model import PetModel
from typing import Callable


def verify_user(_obj, user_id: str) -> UserModel:
    user: UserModel = _obj.session.get(UserModel, user_id)
    if user is None:
        raise DoesNotExistInDatabase("The user does not exist 🤦‍♂️")
    return user


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


def handle_exceptions(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except DataError as e:
            self.session.rollback()
            raise InvalidId() from e
        except IntegrityError as e:
            print(e)
            self.session.rollback()
            raise DuplicatedInDatabase() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise UnknownError() from e
        finally:
            self.session.close()
    return wrapper


def validation_handler(
        user: bool = False,
        pet: bool = False,
        appointment: bool = False
) -> Callable:

    def decorator(func: Callable):
        @handle_exceptions
        def wrapper(self, **kwargs):
            print(kwargs)
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

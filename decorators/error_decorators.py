from errors.exception_classes import InvalidId, DuplicatedInDatabase, UnknownError
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from errors.exception_classes import DoesNotExistInDatabase
from models.appointment_model import AppointmentModel
from sqlalchemy.orm.session import Session
from utils.config_orm import SessionLocal
from models.user_model import UserModel
from models.pet_model import PetModel
from sqlalchemy import and_
from typing import Callable


def check_user(session: Session, user_id: str) -> None:
    if session.get(UserModel, user_id) is None:
        raise DoesNotExistInDatabase("The user does not exist 🤦‍♂️")


def check_pet(session: Session, user_id: str, pet_id: str) -> None:
    pet = session.query(PetModel).where(and_(*[
        PetModel.user_id == user_id,
        PetModel.id == pet_id
    ])).first()

    if pet is None:
        raise DoesNotExistInDatabase("The pet does not exist 🐶")


def check_appointment(
        session: Session,
        user_id: str,
        pet_id: str,
        appointment_id: str
) -> None:
    appointment = session.query(AppointmentModel).where(and_(*[
        AppointmentModel.user_id == user_id,
        AppointmentModel.id == appointment_id,
        AppointmentModel.pet_id == pet_id
    ])).first()

    if appointment is None:
        raise DoesNotExistInDatabase("The appointment does not exist 📑")


def exceptions_handler(
        verify_user: bool = False,
        verify_pet: bool = False,
        verify_appointment: bool = False
):
    def decorator(func: Callable):
        def wrapper(self, *args):
            session = SessionLocal()
            
            try:
                if verify_user:
                    check_user(session, args[0])

                elif verify_pet:
                    check_user(session, args[0])
                    check_pet(session, args[0], args[1])

                elif verify_appointment:
                    check_user(session, args[0])
                    check_pet(session, args[0], args[1])
                    check_appointment(session, args[0], args[1], args[2])

                return func(self, *args)

            except (DataError, IntegrityError, SQLAlchemyError) as e:
                self.session.rollback()

                if isinstance(e, DataError):
                    raise InvalidId() from e

                elif isinstance(e, IntegrityError):
                    raise DuplicatedInDatabase() from e

                elif isinstance(e, SQLAlchemyError):
                    raise UnknownError() from e

            finally:
                session.close()
                self.session.close()

        return wrapper
    return decorator

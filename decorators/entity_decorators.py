from errors.exception_classes import DoesNotExistInDatabase
from models.appointment_model import AppointmentModel
from sqlalchemy.orm.session import Session
from utils.config_orm import SessionLocal
from models.user_model import UserModel
from models.pet_model import PetModel
from typing import Callable
from sqlalchemy import and_

session: Session = SessionLocal()


def check_user(func: Callable) -> Callable:
    def wrapper(*args):
        if session.get(UserModel, args[1]) is None:
            raise DoesNotExistInDatabase("The user does not exist 🤦‍♂️")
        return func(*args)
    return wrapper


def check_pet_context(func: Callable) -> Callable:
    def wrapper(*args):
        pet = session.query(PetModel).where(and_(*[
            PetModel.user_id == args[1],
            PetModel.id == args[2]
        ])).first()

        if pet is None:
            raise DoesNotExistInDatabase("The pet does not exist 🐶")
        return func(*args)
    return wrapper


def check_appointment_context(func: Callable) -> Callable:
    def wrapper(*args):
        appointment = session.query(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == args[1],
            AppointmentModel.id == args[3],
            AppointmentModel.pet_id == args[2]
        ])).first()

        if appointment is None:
            raise DoesNotExistInDatabase("The appointment does not exist 📑")
        return func(*args)
    return wrapper

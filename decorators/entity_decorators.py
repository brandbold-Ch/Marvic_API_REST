from errors.handler_exceptions import handle_do_not_exists
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
            handle_do_not_exists("user")
        return func(*args)
    return wrapper


def check_pet_context(func: Callable) -> Callable:
    def wrapper(*args):
        pet = session.query(PetModel).where(and_(*[
            PetModel.user_id == args[1],
            PetModel.id == args[2]
        ])).first()

        if pet is None:
            handle_do_not_exists("pet")
        return func(*args)
    return wrapper


def check_pet_only(func: Callable) -> Callable:
    def wrapper(*args):
        if session.get(PetModel, args[1]) is None:
            handle_do_not_exists("pet")
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
            handle_do_not_exists("appointment")
        return func(*args)
    return wrapper

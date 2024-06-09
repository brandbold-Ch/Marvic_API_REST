from models.appointment_model import AppointmentModel
from models.user_model import UserModel
from models.pet_model import PetModel
from utils.config_orm import Session
from sqlalchemy.exc import DataError
from sqlalchemy.orm import session
from errors.handler_exceptions import (
    handle_data_error,
    handle_do_not_exists
)


class MWServices:

    def __init__(self) -> None:
        self.session: session.Session = Session()

    def get_user(self, user_id: str) -> None:
        try:
            user = self.session.get(UserModel, user_id)
            if user is None:
                handle_do_not_exists("user")

        except DataError:
            handle_data_error()

    def get_pet(self, pet_id: str) -> None:
        try:
            pet = self.session.get(PetModel, pet_id)
            if pet is None:
                handle_do_not_exists("pet")

        except DataError:
            handle_data_error()

    def get_appointment(self, appointment_id: str) -> None:
        try:
            quote = self.session.get(AppointmentModel, appointment_id)
            if quote is None:
                handle_do_not_exists("appointment")

        except DataError:
            handle_data_error()

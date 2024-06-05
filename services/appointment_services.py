from models.appointment_model import AppointmentModel
from utils.config_orm import Base, engine, Session
from services.mw_services import MWServices
from sqlalchemy.exc import SQLAlchemyError
from models.user_model import UserModel
from models.pet_model import PetModel
from sqlalchemy.exc import DataError
from sqlalchemy.sql import delete
from sqlalchemy import and_
from errors.handler_exceptions import (
    handle_data_error, 
    handle_sqlalchemy_error, 
    handle_do_not_exists
)


class AppointmentServices:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.mw = MWServices()

    def create_appointment(self, user_id: str, pet_id: str, appointment_data: dict) -> None:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)
            appointment_data["user_id"] = user_id
            appointment_data["pet_id"] = pet_id

            self.session.add(AppointmentModel(**appointment_data))
            self.session.commit()

        except DataError:
            self.session.rollback()
            handle_data_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def get_appointment(self, user_id: str, appointment_id: str, pet_id: str) -> dict:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)

            appointment_data = self.session.query(AppointmentModel).filter(and_(*[
                UserModel.id == user_id,
                AppointmentModel.id == appointment_id,
                PetModel.id == pet_id
            ])).first()

            if appointment_data is None:
                handle_do_not_exists("appointment")
            return appointment_data.to_dict()

        except DataError:
            handle_data_error()

        except SQLAlchemyError:
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def get_appointments(self, user_id: str, pet_id: str) -> list[dict]:
        try:
            self.mw.get_user(user_id)
            self.mw.get_pet(pet_id)

            appointments = (self.session.query(AppointmentModel).filter(and_(*[
                UserModel.id == user_id, PetModel.id == pet_id
            ])).all())
            return [appointment.to_dict() for appointment in appointments]

        except DataError:
            handle_data_error()

        except SQLAlchemyError:
            handle_sqlalchemy_error()

        finally:
            self.session.close()

    def delete_appointment(self, user_id: str, appointment_id: str, pet_id: str) -> None:
        try:
            self.get_appointment(user_id, appointment_id, pet_id)

            stmt = delete(AppointmentModel).where(and_(*[
                UserModel.id == user_id,
                AppointmentModel.id == appointment_id,
                PetModel.id == pet_id
            ]))
            self.session.execute(stmt)
            self.session.commit()

        except DataError:
            self.session.rollback()
            handle_data_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

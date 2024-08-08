from decorators.entity_decorators import check_user, check_pet_context, check_appointment_context
from models.appointment_model import AppointmentModel
from decorators.error_decorators import exceptions_handler
from utils.config_orm import Base, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import delete
from sqlalchemy import and_


class AppointmentServices:

    def __init__(self, session: Session):
        Base.metadata.create_all(engine)
        self.session = session

    @check_user
    @check_pet_context
    @exceptions_handler
    def create_appointment(self, user_id: str, pet_id: str, appointment_data: dict) -> dict:
        appointment_create = AppointmentModel(**appointment_data, user_id=user_id, pet_id=pet_id)
        self.session.add(appointment_create)
        self.session.commit()

        return appointment_create.to_dict()

    @check_user
    @check_pet_context
    @check_appointment_context
    @exceptions_handler
    def get_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> dict:
        appointment_data: AppointmentModel | None = self.session.query(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.id == appointment_id,
            AppointmentModel.pet_id == pet_id
        ])).first()

        return appointment_data.to_dict()

    @check_user
    @check_pet_context
    @exceptions_handler
    def get_appointments(self, user_id: str, pet_id: str) -> list[dict]:
        appointments = self.session.query(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.pet_id == pet_id
        ])).all()

        return [appointment.to_dict() for appointment in appointments]

    @check_user
    @check_pet_context
    @check_appointment_context
    @exceptions_handler
    def delete_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> None:
        stmt = delete(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.id == appointment_id,
            AppointmentModel.pet_id == pet_id
        ]))
        self.session.execute(stmt)
        self.session.commit()
   
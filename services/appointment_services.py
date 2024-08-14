from decorators.entity_decorators import check_user, check_pet_context, check_appointment_context
from decorators.error_decorators import exceptions_handler
from models.appointment_model import AppointmentModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import delete
from sqlalchemy import and_


class AppointmentServices:

    def __init__(self, session: Session):
        self.session = session

    @exceptions_handler(verify_pet=True)
    def create_appointment(self, user_id: str, pet_id: str, appointment_data: dict) -> dict:
        appointment_create = AppointmentModel(**appointment_data, user_id=user_id, pet_id=pet_id)
        self.session.add(appointment_create)
        self.session.commit()

        return appointment_create.to_dict()

    @exceptions_handler(verify_appointment=True)
    def get_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> dict:
        appointment_data: AppointmentModel | None = self.session.query(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.id == appointment_id,
            AppointmentModel.pet_id == pet_id
        ])).first()

        return appointment_data.to_dict()

    @exceptions_handler(verify_pet=True)
    def get_appointments(self, user_id: str, pet_id: str) -> list[dict]:
        appointments = self.session.query(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.pet_id == pet_id
        ])).all()

        return [appointment.to_dict() for appointment in appointments]

    @exceptions_handler(verify_appointment=True)
    def delete_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> None:
        stmt = delete(AppointmentModel).where(and_(*[
            AppointmentModel.user_id == user_id,
            AppointmentModel.id == appointment_id,
            AppointmentModel.pet_id == pet_id
        ]))
        self.session.execute(stmt)
        self.session.commit()
   
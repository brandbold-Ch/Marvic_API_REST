from decorators.validator_decorators import entity_validator
from models.appointment_model import AppointmentModel
from utils.load_statics import load_admin_appt_tmpl
from tasks.email_server import mail_sender
from models.stack_model import StackModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from uuid import uuid4
import os

load_dotenv()


class AppointmentServices:

    def __init__(self, session: Session):
        self.session = session

    @entity_validator(pet=True)
    #@pending_appt_hecker
    def create_appointment(self, **kwargs) -> dict:
        appointment_create = AppointmentModel(
            **kwargs.get("appointment_data"),
            pet_id=kwargs.get("pet_id"),
            user_id=kwargs.get("user_id")
        )

        self.session.add(appointment_create)
        self.session.add(
            StackModel(
                id=uuid4(),
                appointment_id=appointment_create.id
            )
        )
        self.session.commit()

        mail_sender.delay(
            load_admin_appt_tmpl(
                appt_id=str(appointment_create.id),
                issue=appointment_create.issue,
                created_at=str(appointment_create.created_at),
                timestamp=str(appointment_create.timestamp)
            ),
            "Nueva cita agendada",
            os.getenv("ADMIN_RECIPIENT_EMAIL")
        )

        return appointment_create.to_dict()

    @entity_validator(appointment=True)
    def get_appointment(self, **kwargs) -> dict:
        appointment_data: AppointmentModel = kwargs.get("object_result")
        return appointment_data.to_dict()

    @entity_validator(pet=True)
    def get_appointments(self, **kwargs) -> list[dict]:
        appointments: list[AppointmentModel] = kwargs.get(
            "object_result"
        ).appointments

        return [appointment.to_dict() for appointment in appointments]

    @entity_validator(appointment=True)
    def delete_appointment(self, **kwargs) -> None:
        self.session.delete(kwargs.get("object_result"))
        self.session.commit()
   
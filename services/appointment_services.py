from decorators.validator_decorators import entity_validator
from models.appointment_model import AppointmentModel
from sqlalchemy.orm import Session


class AppointmentServices:

    def __init__(self, session: Session):
        self.session = session

    @entity_validator(pet=True)
    def create_appointment(self, **kwargs) -> dict:
        appointment_create = AppointmentModel(
            **kwargs.get("appointment_data"),
            pet_id=kwargs.get("pet_id"),
            user_id=kwargs.get("user_id")
        )
        self.session.add(appointment_create)
        self.session.commit()

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
   
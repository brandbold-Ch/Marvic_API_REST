from decorators.error_decorators import validation_handler
from models.appointment_model import AppointmentModel
from models.pet_model import PetModel
from sqlalchemy.orm import Session


class AppointmentServices:

    def __init__(self, session: Session):
        self.session = session

    @validation_handler(pet=True)
    def create_appointment(self, **kwargs) -> dict:
        appointment_create = AppointmentModel(
            **kwargs.get("appointment_data"),
            pet_id=kwargs.get("pet_id"),
            user_id=kwargs.get("user_id")
        )
        self.session.add(appointment_create)
        self.session.commit()

        return appointment_create.to_dict()

    @validation_handler(appointment=True)
    def get_appointment(self, **kwargs) -> dict:
        appointment_data: AppointmentModel = kwargs.get("object_result")
        return appointment_data.to_dict()

    @validation_handler(pet=True)
    def get_appointments(self, **kwargs) -> list[dict]:
        appointments: list[AppointmentModel] = kwargs.get(
            "object_result"
        ).appointments

        return [appointment.to_dict() for appointment in appointments]

    @validation_handler(appointment=True)
    def delete_appointment(self, **kwargs) -> None:
        self.session.delete(kwargs.get("object_result"))
        self.session.commit()
   
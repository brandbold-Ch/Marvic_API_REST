from services.appointment_services import AppointmentServices
from sqlalchemy.orm import Session


class AppointmentControllers:

    def __init__(self, session: Session) -> None:
        self.appointment = AppointmentServices(session)

    def create_appointment(self, user_id: str, pet_id: str, appointment_data: dict) -> dict:
        return self.appointment.create_appointment(user_id, pet_id, appointment_data)

    def get_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> dict:
        return self.appointment.get_appointment(user_id, pet_id, appointment_id)

    def get_appointments(self, user_id: str, pet_id: str) -> list[dict]:
        return self.appointment.get_appointments(user_id, pet_id)

    def delete_appointment(self, user_id: str, pet_id: str, appointment_id: str) -> None:
        self.appointment.delete_appointment(user_id, pet_id, appointment_id)

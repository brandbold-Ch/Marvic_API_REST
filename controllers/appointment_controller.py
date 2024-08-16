from services.appointment_services import AppointmentServices
from sqlalchemy.orm import Session


class AppointmentControllers:

    def __init__(self, session: Session) -> None:
        self.appointment = AppointmentServices(session)

    def create_appointment(self, **kwargs) -> dict:
        return self.appointment.create_appointment(**kwargs)

    def get_appointment(self, **kwargs) -> dict:
        return self.appointment.get_appointment(**kwargs)

    def get_appointments(self, **kwargs) -> list[dict]:
        return self.appointment.get_appointments(**kwargs)

    def delete_appointment(self, **kwargs) -> None:
        self.appointment.delete_appointment(**kwargs)

from services.appointment_services import AppointmentServices


class AppointmentControllers:

    def __init__(self) -> None:
        self.service = AppointmentServices()

    def create_appointment(self, user_id: str, pet_id: str, appointment_data: dict) -> None:
        self.service.create_appointment(user_id, pet_id, appointment_data)

    def get_appointment(self, user_id: str, appointment_id: str, pet_id: str) -> dict:
        return self.service.get_appointment(user_id, appointment_id, pet_id)

    def get_appointments(self, user_id: str, pet_id: str) -> list[dict]:
        return self.service.get_appointments(user_id, pet_id)

    def delete_appointment(self, user_id: str, appointment_id: str, pet_id: str) -> None:
        self.service.delete_appointment(user_id, appointment_id, pet_id)

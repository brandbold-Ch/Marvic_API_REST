from decorators.validator_decorators import entity_validator, appointment_checker
from models.appointment_model import AppointmentModel
from utils.notify_email import notify_admin
from utils.image_tools import delete_image
from models.stack_model import StackModel
from sqlalchemy.orm import Session
from uuid import uuid4


class AppointmentServices:

    def __init__(self, session: Session):
        self.session = session

    @entity_validator(pet=True)
    @appointment_checker
    def create_appointment(self, **kwargs) -> dict:
        appointment_create = AppointmentModel(
            **kwargs.get("appointment_data"),
            pet_id=kwargs.get("pet_id"),
            user_id=kwargs.get("user_id")
        )
        
        self.session.add(appointment_create)
        self.session.add(StackModel(
            id=uuid4(),
            appointment_id=appointment_create.id
        ))
        self.session.commit()
        
        notify_admin(
            appt_id=appointment_create.id,
            issue=appointment_create.issue,
            created_at=appointment_create.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
            timestamp=appointment_create.timestamp.strftime("%Y-%m-%d %I:%M:%S %p"),
            price=appointment_create.price
        )
        
        return appointment_create.to_dict()

    @entity_validator(appointment=True)
    def get_appointment(self, **kwargs) -> dict:
        appointment_data: AppointmentModel = kwargs.get("object_result")
        return appointment_data.to_dict()

    @entity_validator(pet=True)
    def get_appointments(self, **kwargs) -> list[dict]:
        appointments: list[AppointmentModel] = kwargs.get("object_result").appointments
        return [appointment.to_dict() for appointment in appointments]

    @entity_validator(appointment=True)
    def delete_appointment(self, **kwargs) -> None:
        medical_history = kwargs.get("object_result").to_dict()
        array_images = medical_history["medical_history"]
        
        self.session.delete(kwargs.get("object_result"))
        self.session.commit()
        
        if array_images is not None:
            try:
                for image in array_images["images"]:
                    image_tag = image.split("/")
                    delete_image(image_tag[-1])
            except:
                pass
            
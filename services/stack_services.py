from decorators.validator_decorators import verify_auth_by_id
from decorators.error_decorators import handle_exceptions
from models.appointment_model import AppointmentModel
from models.stack_model import StackModel
from models.pet_model import PetModel
from sqlalchemy.orm import Session


class StackServices:

    def __init__(self, session: Session):
        self.session = session

    @handle_exceptions
    def get_stack(self, stack_id: str) -> dict | None:
        stack = self.session.get(StackModel, stack_id)
        if stack is not None:
            return {
                "ref": stack,
                "parsed": stack.to_dict()
            }

    @handle_exceptions
    def get_stacks(self) -> list:
        stacks = self.session.query(StackModel).all()
        return stacks

    @handle_exceptions
    def delete_stack(self, stack_obj: StackModel) -> None:
        self.session.delete(stack_obj)
        self.session.commit()

    @handle_exceptions
    def get_appointment(self, appointment_id: str) -> tuple:
        appointment_data = self.session.get(AppointmentModel, appointment_id)
        pet_data = self.session.get(PetModel, appointment_data.pet_id)
        auth_data = verify_auth_by_id(self, pet_data.user_id, "USER")
        
        return appointment_data, pet_data, auth_data
        
    @handle_exceptions
    def update_appointment(self, appt_obj: AppointmentModel) -> None:
        self.session.add(appt_obj)
        self.session.commit()

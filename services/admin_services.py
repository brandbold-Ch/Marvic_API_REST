from models.medical_history_model import MedicalHistoryModel
from decorators.validator_decorators import entity_validator
from decorators.error_decorators import handle_exceptions
from models.appointment_model import AppointmentModel
from utils.image_tools import upload_image
from sqlalchemy.orm.session import Session
from models.admin_model import AdminModel
from models.image_model import ImageModel
from models.auth_model import AuthModel
from models.user_model import UserModel
from models.pet_model import PetModel
from decorators.validator_decorators import (
    entity_validator, 
    verify_auth_by_email
)
from errors.exception_classes import (
    DbNotFoundError, 
    DataValidationError, 
    DuplicatedMedicalHistory
)
import bcrypt
from uuid import uuid4


class AdminServices:

    def __init__(self, session: Session):
        self.session = session

    @handle_exceptions
    def create_admin(self, **kwargs) -> None:
        admin_search = self.session.query(AdminModel).all()
        admin_data = kwargs.get("admin_data")
        auth_data = kwargs.get("auth_data")
        
        if len(admin_search) == 0:
            admin_create = AdminModel(**admin_data)
            auth_create = AuthModel(**auth_data, admin_id=admin_create.id)

            self.session.add(admin_create)
            self.session.add(auth_create)
            self.session.commit()
            
    @entity_validator(admin=True)
    def update_admin(self, **kwargs) -> dict:
        admin_update: AdminModel = kwargs.get("object_result")
        admin_data = kwargs.get("admin_data")
        del admin_data["id"]
        
        admin_update.update_fields(**admin_data)
        self.session.add(admin_update)
        self.session.commit()
        
        return admin_update.to_dict()
    
    @entity_validator(admin=True)
    def get_admin(self, **kwargs) -> dict:
        admin_data: AdminModel = kwargs.get("object_result")
        return admin_data.to_dict()
    
    @handle_exceptions
    def get_unique_admin(self) -> dict | None:
        admin = self.session.query(AdminModel).first()
        
        if admin:
            return admin.to_dict()
        return None
    
    @handle_exceptions
    def get_pets(self) -> list[dict]:
        pets = self.session.query(PetModel).all()
        return [pet.to_dict() for pet in pets]
    
    @handle_exceptions       
    def get_users(self) -> list[dict]:
        users = self.session.query(UserModel).all()
        return [user.to_dict() for user in users]
    
    @handle_exceptions
    def get_appointments(self) -> list[dict]:
        appointments = self.session.query(AppointmentModel).all()
        return [appointment.to_dict() for appointment in appointments]
    
    @handle_exceptions
    def get_pet(self, pet_id: str) -> dict:
        pet = self.session.get(PetModel, pet_id)
        
        if pet is None:
            raise DbNotFoundError("The pet does not exist 🐶")
        return pet.to_dict()
    
    @handle_exceptions       
    def get_user(self, user_id: str) -> dict:
        user = self.session.get(UserModel, user_id)
        
        if user is None:
            raise DbNotFoundError("The user does not exist 🤦‍♂️")
        return user.to_dict()
    
    @handle_exceptions
    def get_appointment(self, appointment_id: str) -> dict:
        appointment = self.session.get(AppointmentModel, appointment_id)

        if appointment is None:
            raise DbNotFoundError("The appointment does not exist 📑")
        
        user = self.session.get(UserModel, appointment.user_id)
        pet = self.session.get(PetModel, appointment.pet_id)
        
        return {
            "appointment_data": appointment.to_dict(),
            "pet_data": pet.to_dict(),
            "user_data": user.to_dict()
        }
    
    @handle_exceptions
    def change_password_to_user(self, **kwargs) -> dict:
        auth_update: AuthModel = verify_auth_by_email(
            self, kwargs.get("email")
        )
        auth_update.password = bcrypt.hashpw(
            kwargs.get("new_password").encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")
        self.session.add(auth_update)
        self.session.commit()

        return auth_update.to_dict()
    
    async def create_medical_history(self, **kwargs) -> dict:
        appt = kwargs.get("appointment_id")
        appointment = self.session.get(AppointmentModel, appt)

        if appointment is None:
            raise DbNotFoundError("The appointment does not exist 📑")
        
        validation_items = (self.session
            .query(MedicalHistoryModel)
            .where(MedicalHistoryModel.appointment_id == appt)
        ).all()
        
        if len(validation_items) == 1:
            raise DuplicatedMedicalHistory()
                
        medical_history_create = MedicalHistoryModel(
            id=uuid4(),
            appointment_id=appt,
            issue=kwargs.get("issue")
        )
        self.session.add(medical_history_create)
        self.session.commit()
                        
        if kwargs.get("images") is not None:
            for image in kwargs.get("images"):
                image_path = await upload_image(image)
                self.session.add(
                    ImageModel(
                        id=uuid4(), 
                        image=image_path,
                        medical_history_id=medical_history_create.id
                    )
                )
                self.session.commit()
        
        return medical_history_create.to_dict()
        
    @handle_exceptions
    def update_appointment(self, appointment_id: str, state: str) -> dict:
        appointment_update = self.session.get(AppointmentModel, appointment_id)
        status_choices = ["pending", "completed", "canceled"]

        if appointment_update is None:
            raise DbNotFoundError("The appointment does not exist 📑")
        
        elif state in status_choices:
            appointment_update.status = state
            appointment_update.expired = True
            self.session.add(appointment_update)
            self.session.commit()
            
            return appointment_update.to_dict()
        
        raise DataValidationError(detail="must be [pending, completed, cancelled]")

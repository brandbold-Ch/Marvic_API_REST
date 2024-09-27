from decorators.error_decorators import handle_exceptions
from models.appointment_model import AppointmentModel
from errors.exception_classes import DbNotFoundError
from sqlalchemy.orm.session import Session
from models.admin_model import AdminModel
from models.auth_model import AuthModel
from models.user_model import UserModel
from models.pet_model import PetModel
from decorators.validator_decorators import (
    entity_validator, 
    verify_auth_by_email
)
import bcrypt


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
        return appointment.to_dict()
    
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
    
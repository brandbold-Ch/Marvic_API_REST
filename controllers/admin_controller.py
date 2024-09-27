from services.admin_services import AdminServices
from sqlalchemy.orm import Session


class AdminControllers:

    def __init__(self, session: Session) -> None:
        self.admin = AdminServices(session)
        
    def create_admin(self, **kwargs) -> None:
        self.admin.create_admin(**kwargs)
        
    def update_admin(self, **kwargs) -> dict:
        return self.admin.update_admin(**kwargs)
    
    def get_admin(self, **kwargs) -> dict:
        return self.admin.get_admin(**kwargs)
    
    def get_users(self, **kwargs) -> list[dict]:
        return self.admin.get_users(**kwargs)
    
    def get_pets(self, **kwargs) -> list[dict]:
        return self.admin.get_pets(**kwargs)
    
    def get_appointments(self, **kwargs) -> list[dict]:
        return self.admin.get_appointments(**kwargs)
    
    def get_user(self, user_id) -> dict:
        return self.admin.get_user(user_id)
    
    def get_pet(self, pet_id: str) -> dict:
        return self.admin.get_pet(pet_id)
    
    def get_appointment(self, appointment_id: str) -> dict:
        return self.admin.get_appointment(appointment_id)
    
    def change_password_to_user(self, **kwargs) -> dict:
        return self.admin.change_password_to_user(**kwargs)

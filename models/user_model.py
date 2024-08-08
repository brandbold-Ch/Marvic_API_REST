from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from utils.config_orm import Base


class UserModel(Base):

    __tablename__ = "user"
    id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False)
    auth = relationship("AuthModel", uselist=False, cascade="all, delete")
    pets = relationship("PetModel", cascade="all, delete-orphan")

    def update_fields(self, **kwargs) -> None:
        for name, value in kwargs.items():
            setattr(self, name, value)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "lastname": self.lastname,
            "phone_number": self.phone_number,
            "auth_data": {
                "id": str(self.auth.id),
                "user_id": str(self.auth.user_id),
                "email": self.auth.email,
                "password": self.auth.password,
                "role": self.auth.role
            }
        }

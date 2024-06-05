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
    pets = relationship("PetModel", cascade="all, delete")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "lastname": self.lastname,
            "phone_number": self.phone_number
        }

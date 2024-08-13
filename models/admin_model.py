from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship
from utils.config_orm import Base


class AdminModel(Base):

    __tablename__ = "admin"
    id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    occupation = Column(String(60), nullable=True)
    auth = relationship(
        "AuthModel",
        uselist=False,
        cascade="all, delete"
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "lastname": self.lastname,
            "occupation": self.occupation,
            "auth_data": {
                "id": str(self.auth.id),
                "user_id": str(self.auth.user_id),
                "email": self.auth.email,
                "password": self.auth.password,
                "role": self.auth.role
            }
        }

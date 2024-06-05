from sqlalchemy import Column, String, UUID, ForeignKey
from utils.config_orm import Base


class AuthModel(Base):

    __tablename__ = "auth"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(13), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "email": self.email,
            "password": self.password,
            "role": self.role
        }

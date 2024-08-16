from sqlalchemy import Column, String, UUID, ForeignKey
from schemas.auth_schema import Auth
from .admin_model import AdminModel
from utils.config_orm import Base


class AuthModel(Base):

    __tablename__ = "auth"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), unique=True, nullable=True)
    admin_id = Column(UUID, ForeignKey("admin.id"), nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(13), nullable=False)

    def update_credentials(self, **kwargs) -> None:
        for field, value in kwargs.items():
            setattr(self, field, value)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "email": self.email,
            "password": self.password,
            "role": self.role
        }

from sqlalchemy import Column, String, UUID, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from utils.config_orm import Base


class AuthModel(Base):

    __tablename__ = "auth"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(ARRAY(String), default=["USER"])
    user = relationship("UserModel", back_populates="auth")

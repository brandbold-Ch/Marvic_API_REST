from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from utils.config_orm import Base
from uuid import uuid4


class User(Base):

    __tablename__ = "user"
    id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone_number = Column(String(10), nullable=False)
    auth = relationship("Auth", uselist=False, back_populates="user")

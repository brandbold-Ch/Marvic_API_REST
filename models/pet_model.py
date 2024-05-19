from sqlalchemy import Column, Boolean, Float, String, UUID, ForeignKey
from utils.config_orm import Base
from uuid import uuid4


class Pet(Base):

    __tablename__ = "Pet"
    id = Column(UUID, primary_key=True, default=uuid4())
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False, unique=True),
    name = Column(String(30))
    specie = Column(String(5), nullable=False)
    gender = Column(String(6), nullable=False)
    size = Column(String(7), nullable=True)
    age = Column(String(20), nullable=True)
    breed = Column(String(60), nullable=True)
    weight = Column(Float, nullable=True)
    live = Column(Boolean, default=True)

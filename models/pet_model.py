from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from utils.config_orm import Base
from uuid import uuid4


class Pet(Base):

    __tablename__ = "Pet"
    id = Column(UUID, primary_key=True, default=uuid4())

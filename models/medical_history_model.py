from sqlalchemy import Column, Text, UUID, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from utils.config_orm import Base


class MedicalHistoryModel(Base):

    __tablename__ = "medical_history"
    id = Column(UUID, primary_key=True)
    issue = Column(Text, nullable=True)
    pet_id = Column(UUID, ForeignKey("pet.id"))

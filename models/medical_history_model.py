from sqlalchemy import Column, Text, UUID, ForeignKey
from utils.config_orm import Base


class MedicalHistoryModel(Base):

    __tablename__ = "medical_history"
    id = Column(UUID, primary_key=True)
    issue = Column(Text, nullable=True)
    pet_id = Column(UUID, ForeignKey("pet.id"), nullable=False)
    staff_id = Column(UUID, ForeignKey("staff.id"), nullable=False)

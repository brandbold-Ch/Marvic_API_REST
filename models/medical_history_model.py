from sqlalchemy import Column, Text, UUID, ForeignKey
from utils.config_orm import Base


class MedicalHistoryModel(Base):

    __tablename__ = "medical_history"
    id = Column(UUID, primary_key=True)
    issue = Column(Text, nullable=True)
    pet_id = Column(UUID, ForeignKey("pet.id"), nullable=False)
    staff_id = Column(UUID, ForeignKey("staff.id"), nullable=False)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "issue": self.issue,
            "pet_id": str(self.pet_id),
            "staff_id": str(self.staff_id)
        }
    
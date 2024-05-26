from sqlalchemy import Column, Text, Boolean, UUID, Date, ForeignKey, String
from utils.config_orm import Base
from datetime import datetime



class StaffModel(Base):
    
    __tablename__ = "staff"
    id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    academic_studies = Column(String(70), nullable=True)
    
    
    def to_representation(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "lastname": self.lastname,
            "academic_studies": self.academic_studies
        }
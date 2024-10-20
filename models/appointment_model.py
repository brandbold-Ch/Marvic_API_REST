from sqlalchemy.orm import relationship
from utils.config_orm import Base
from sqlalchemy import (
    Column, 
    Text, 
    String, 
    UUID, 
    ForeignKey, 
    Float, 
    DateTime, 
    Boolean
)
import os


class AppointmentModel(Base):

    __tablename__ = "appointment"
    id = Column(UUID, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    pet_id = Column(UUID, ForeignKey("pet.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    issue = Column(Text, nullable=True)
    status = Column(String(10), nullable=False)
    price = Column(Float, nullable=True)
    expired = Column(Boolean, nullable=False)
    medical_history = relationship(
        "MedicalHistoryModel",
        back_populates="appointment", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    def get_medical_history(self) -> dict | None:
        if self.medical_history is None:
            return None
        return self.medical_history.to_dict()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "dates": {
                "creation_date": str(self.created_at.strftime("%Y-%m-%d %I:%M:%S %p")),
                "expiration_date": str(self.timestamp.strftime("%Y-%m-%d %I:%M:%S %p")),
            },
            "relationships": {
                "pet_id": str(self.pet_id),
                "user_id": str(self.user_id)
            },
            "details": {
                "issue": self.issue,
                "status": self.status,
                "price": self.price,
                "expired": self.expired
            },
            "medical_history": self.get_medical_history()
        }

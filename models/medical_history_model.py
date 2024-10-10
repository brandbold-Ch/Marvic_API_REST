from sqlalchemy import Column, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship
from utils.config_orm import Base
import os


class MedicalHistoryModel(Base):
    __tablename__ = "medical_history"
    
    id = Column(UUID, primary_key=True)
    appointment_id = Column(UUID, ForeignKey("appointment.id"), nullable=False)
    issue = Column(Text, nullable=True)    
    images = relationship(
        "ImageModel",
        backref="medical_history",
        uselist=True,
        cascade="all, delete-orphan"
    )
    appointment = relationship(
        "AppointmentModel",
        back_populates="medical_history",
        uselist=False
    )
    
    def get_images(self) -> list:
        if self.images is not None:
            return [
                f"{os.getenv('GET_IMAGE_URL')}{image.image}" for image in self.images
            ]
        return []

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "issue": self.issue,
            "appointment_id": str(self.appointment_id),
            "images": self.get_images(),
        }

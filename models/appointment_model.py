from sqlalchemy import Column, Text, String, UUID, Date, ForeignKey, Float
from utils.config_orm import Base
from datetime import datetime


class AppointmentModel(Base):

    __tablename__ = "appointment"
    id = Column(UUID, primary_key=True)
    creation_date = Column(Date, default=datetime.now())
    expiration_date = Column(Date, nullable=False)
    pet_id = Column(UUID, ForeignKey("pet.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    issue = Column(Text, nullable=True)
    status = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "dates": {
                "creation_date": str(self.creation_date),
                "expiration_date": str(self.expiration_date),
            },
            "relationships": {
                "pet_id": str(self.pet_id),
                "user_id": str(self.user_id)
            },
            "details": {
                "issue": self.issue,
                "status": self.status,
                "price": self.price
            }
        }

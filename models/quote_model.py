from sqlalchemy import Column, Text, Boolean, UUID, Date, ForeignKey
from utils.config_orm import Base, Session
from datetime import datetime


class QuoteModel(Base):

    __tablename__ = "quote"
    id = Column(UUID, primary_key=True)
    creation_date = Column(Date, default=datetime.now())
    expiration_date = Column(Date, nullable=False)
    pet_id = Column(UUID, ForeignKey("pet.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    issue = Column(Text, nullable=True)
    solved = Column(Boolean, default=False)

    def to_representation(self) -> dict:
        return {
            "id": str(self.id),
            "creation_date": str(self.creation_date),
            "expiration_date": str(self.expiration_date),
            "pet_id": str(self.pet_id),
            "user_id": str(self.user_id),
            "issue": self.issue,
            "solved": self.solved
        }

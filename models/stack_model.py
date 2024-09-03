from sqlalchemy import Column, UUID
from utils.config_orm import Base


class StackModel(Base):

    __tablename__ = "stack"
    id = Column(UUID, primary_key=True)
    appointment_id = Column(UUID, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "appointment_id": str(self.appointment_id)
        }

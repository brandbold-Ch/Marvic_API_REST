from sqlalchemy import Column, String, UUID, ForeignKey
from utils.config_orm import Base


class ImageModel(Base):
    
    __tablename__ = "image"
    id = Column(UUID, primary_key=True)
    image = Column(String(70), nullable=False)
    pet_id = Column(UUID, nullable=True, unique=True)
    medical_history_id = Column(UUID, nullable=True)
    
    def to_representation(self) -> dict:
        return {
            "id": str(self.id),
            "image": self.image,
            "pet_id": str(self.id),
            "medical_history_id": str(self.medical_history_id)
        }
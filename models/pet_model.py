from sqlalchemy import Column, Boolean, Float, String, UUID, ForeignKey
from utils.config_orm import Base


class PetModel(Base):

    __tablename__ = "pet"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    name = Column(String(30))
    specie = Column(String(5), nullable=False)
    gender = Column(String(6), nullable=False)
    size = Column(String(7), nullable=True)
    age = Column(String(20), nullable=True)
    breed = Column(String(60), nullable=True)
    weight = Column(Float, nullable=True)
    is_live = Column(Boolean, default=True)

    def to_representation(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "specie": self.specie,
            "gender": self.gender,
            "size": self.size,
            "age": self.age,
            "breed": self.breed,
            "weight": self.weight,
            "is_live": self.is_live
        }

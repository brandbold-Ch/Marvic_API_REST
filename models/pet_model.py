from sqlalchemy import Column, Boolean, Float, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from utils.config_orm import Base


class PetModel(Base):

    __tablename__ = "pet"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    name = Column(String(25), nullable=True)
    specie = Column(String(5), nullable=False)
    gender = Column(String(6), nullable=False)
    size = Column(String(7), nullable=True)
    age = Column(String(20), nullable=True)
    breed = Column(String(60), nullable=True)
    weight = Column(Float, nullable=True)
    is_live = Column(Boolean, default=True)
    image = relationship("ImageModel", uselist=False, backref="pet")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "basic_info": {
                "name": self.name,
                "specie": self.specie,
                "breed": self.breed
            },
            "appearance": {
                "gender": self.gender,
                "size": self.size,
                "weight": self.weight,
                "image": self.image.image if self.image is not None else None
            },
            "additional_details": {
                "age": self.age,
                "is_live": self.is_live
            }
        }

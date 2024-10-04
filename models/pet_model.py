from sqlalchemy import Column, Float, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from utils.config_orm import Base
import os


class PetModel(Base):

    __tablename__ = "pet"
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    name = Column(String(25), nullable=True)
    specie = Column(String(5), nullable=True)
    gender = Column(String(6), nullable=True)
    size = Column(String(7), nullable=True)
    age = Column(String(20), nullable=True)
    breed = Column(String(60), nullable=True)
    weight = Column(Float, nullable=True)
    appointments = relationship(
        "AppointmentModel",
        cascade="all, delete-orphan"
    )
    image = relationship(
        "ImageModel",
        uselist=False,
        backref="pet",
        cascade="all, delete-orphan"
    )

    def get_image(self) -> str | None:
        if self.image is not None:
            return f"{os.getenv('GET_IMAGE_URL')}{self.image.image}"
        return None

    def update_fields(self, **kwargs) -> None:
        for field, value in kwargs.items():
            setattr(self, field, value)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "basic_info": {
                "name": self.name,
                "specie": self.specie,
                "breed": self.breed,
                "age": self.age
            },
            "appearance": {
                "gender": self.gender,
                "size": self.size,
                "weight": self.weight,
                "image": self.get_image()
            }
        }

from sqlalchemy import Column, UUID, String
from utils.config_orm import Base


class StaffModel(Base):

    __tablename__ = "staff"
    id = Column(UUID, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    academic_studies = Column(String(70), nullable=True)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "lastname": self.lastname,
            "academic_research": self.academic_studies
        }

from sqlalchemy import Column, UUID, JSON
from utils.config_orm import Base



class PriceModel(Base):

    __tablename__ = "price"
    id = Column(UUID, primary_key=True)
    prices = Column(JSON, nullable=False)


    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "prices": self.prices
        }
    
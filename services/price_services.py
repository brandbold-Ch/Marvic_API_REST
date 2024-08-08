from utils.config_orm import Base, engine, SessionLocal
from models.price_model import PriceModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DataError
from sqlalchemy import and_, update
from errors.handler_exceptions import (
    handle_sqlalchemy_error,
    handle_do_not_exists,
    handle_data_error
)


class PriceService:

    def __init__(self) -> None:
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def get_price(self, price_id: str) -> dict:
        try:
            price = self.session.query(PriceModel).get(price_id)

            if price is None:
                handle_do_not_exists("price")
            return price.to_dict()
        
        except DataError:
            handle_data_error()

        except SQLAlchemyError:
            handle_sqlalchemy_error()

        finally:
            self.session.close()
        
    def update_price(self, price_id: str, price_data: dict) -> None:
        try:
           self.get_price(price_id)

           stmt = (update(PriceModel)
                   .where(and_(*[PriceModel.id == price_id]))
                   .values(prices=price_data))
           self.session.execute(stmt)
           self.session.commit()
        
    
        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()

from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from errors.handler_exceptions import (
    handle_sqlalchemy_error, 
    handle_integrity_error,
    handle_data_error
)
from typing import Callable

    
def exceptions_handler(func: Callable):
    def wrapper(self, *args):
        try:
            return func(self, *args)

        except DataError:
            self.session.rollback()
            handle_data_error()

        except IntegrityError:
            self.session.rollback()
            handle_integrity_error()

        except SQLAlchemyError:
            self.session.rollback()
            handle_sqlalchemy_error()

        finally:
            self.session.close()
    return wrapper

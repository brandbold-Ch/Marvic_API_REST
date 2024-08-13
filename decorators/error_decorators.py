from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from errors.exception_classes import InvalidId, DuplicatedInDatabase, UnknownError
from typing import Callable

    
def exceptions_handler(func: Callable):
    def wrapper(self, *args):
        try:
            return func(self, *args)

        except DataError as e:
            self.session.rollback()
            raise InvalidId() from e

        except IntegrityError as e:
            self.session.rollback()
            raise DuplicatedInDatabase() from e

        except SQLAlchemyError as e:
            self.session.rollback()
            raise UnknownError() from e

        finally:
            self.session.close()
    return wrapper

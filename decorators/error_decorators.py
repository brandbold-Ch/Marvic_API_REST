from errors.exception_classes import InvalidId, DuplicatedInDatabase, UnknownError
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from typing import Callable


def handle_exceptions(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except DataError as e:
            self.session.rollback()
            raise InvalidId() from e
        except IntegrityError as e:
            print(e)
            self.session.rollback()
            raise DuplicatedInDatabase() from e
        except SQLAlchemyError as e:
            self.session.rollback()
            raise UnknownError(detail=e) from e
        finally:
            self.session.close()
    return wrapper

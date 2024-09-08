from errors.exception_classes import DbInvalidFormatIdError, DbDuplicatedKeyError, ServerUnknownError
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from typing import Callable


def handle_exceptions(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except DataError as e:
            self.session.rollback()
            raise DbInvalidFormatIdError() from e

        except IntegrityError as e:
            self.session.rollback()
            raise DbDuplicatedKeyError() from e

        except SQLAlchemyError as e:
            self.session.rollback()
            raise ServerUnknownError(detail=e) from e

        finally:
            self.session.close()
    return wrapper

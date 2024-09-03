from errors.exception_classes import (
    DbNotFoundError,
    DbDuplicatedKeyError,
    DbInvalidFormatIdError
)


def handle_integrity_error() -> None:
    raise DbDuplicatedKeyError("That account already exists")


def handle_data_error() -> None:
    raise DbInvalidFormatIdError("UUID with invalid format 🆔")


def handle_do_not_exists(model_name: str) -> None:
    raise DbNotFoundError(f"The {model_name} does not exist ❌")


def handle_sqlalchemy_error() -> None:
    raise Exception("There was a conflict in the database query ⚠️")

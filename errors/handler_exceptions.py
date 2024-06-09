from errors.exception_classes import (
    DoesNotExistInDatabase,
    DuplicatedInDatabase, 
    InvalidUUID
)


def handle_integrity_error() -> None:
    raise DuplicatedInDatabase("That account already exists")

def handle_data_error() -> None:
    raise InvalidUUID("UUID with invalid format 🆔") 

def handle_do_not_exists(model_name: str) -> None:
    raise DoesNotExistInDatabase(f"The {model_name} does not exist ❌")

def handle_sqlalchemy_error() -> None:
    raise Exception("There was a conflict in the database query ⚠️")

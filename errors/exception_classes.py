from typing import Any


class DuplicatedInDatabase(Exception):
    def __init__(self, message: Any):
        super().__init__(message)


class EntityNotExist(Exception):
    def __init__(self, message: Any):
        super().__init__(message)


class DoesNotExistInDatabase(Exception):
    def __init__(self, message: Any):
        super().__init__(message)


class InvalidUUID(Exception):
    def __init__(self, message: Any):
        super().__init__(message)

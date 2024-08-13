from utils.status_codes import error_codes, status_codes
from typing import Any


class ServerBaseException(Exception):

    def __init__(self, message: Any) -> None:
        super().__init__(message)
        self.original_message = str(message)
        self.http_argument = ""
        self.error_code = 0
        self.status_code = 0

    def to_dict(self) -> dict:
        return {
            "status": self.http_argument,
            "message": self.original_message,
            "details": self.__dict__["__notes__"][0].strip(),
            "codes": {
                "status_code": self.status_code,
                "error_code": self.error_code
            }
        }


class DuplicatedInDatabase(ServerBaseException):
    def __init__(self, message="That user already exists in the database 🔂") -> None:
        super().__init__(message)
        self.add_note("""
            El usuario que intentas crear ya existe en la base de datos.
        """)
        self.error_code = error_codes["DB_DUPLICATED_KEY"]
        self.status_code = status_codes["CONFLICT"]
        self.http_argument = "Conflict 💥"


class DoesNotExistInDatabase(ServerBaseException):
    def __init__(self, message="Does not exist in the database 🤦‍♂️") -> None:
        super().__init__(message)
        self.add_note("""
            La identidad que buscas no existe en la base de datos.
        """)
        self.error_code = error_codes["DB_NOT_FOUND"]
        self.status_code = status_codes["NOT_FOUND"]
        self.http_argument = "Not Found 🚫"


class InvalidId(ServerBaseException):
    def __init__(self, message="The Id is invalid, must be UUID 🆔") -> None:
        super().__init__(message)
        self.add_note("""
            El id que mandas no es el adecuado, debe ser un UUID.
        """)
        self.error_code = error_codes["DB_INVALID_FORMAT_ID"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class ErrorInFields(ServerBaseException):
    def __init__(self, message="There are errors in the fields ⚠️") -> None:
        super().__init__(message)
        self.add_note("""
            Alguno de los campos no tiene el tipo correcto.
        """)
        self.error_code = error_codes["ERROR_DATA_VALIDATION"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class UnknownError(ServerBaseException):
    def __init__(self, message="Unknown error ❌") -> None:
        super().__init__(message)
        self.add_note("""
            Hubo un error en el servidor.
        """)
        self.error_code = error_codes["SERVER_UNKNOWN_ERROR"]
        self.status_code = status_codes["INTERNAL_SERVER_ERROR"]
        self.http_argument = "Internal Server Error 💀"

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


class DbDuplicatedKeyError(ServerBaseException):
    def __init__(self, message="That user already exists in the database 🔂") -> None:
        super().__init__(message)
        self.add_note("""
            El usuario que intentas crear ya existe en la base de datos.
        """)
        self.error_code = error_codes["DB_DUPLICATED_KEY"]
        self.status_code = status_codes["CONFLICT"]
        self.http_argument = "Conflict 💥"


class DbNotFoundError(ServerBaseException):
    def __init__(self, message="Does not exist in the database 🤦‍♂️") -> None:
        super().__init__(message)
        self.add_note("""
            La identidad que buscas no existe en la base de datos.
        """)
        self.error_code = error_codes["DB_NOT_FOUND"]
        self.status_code = status_codes["NOT_FOUND"]
        self.http_argument = "Not Found 🚫"


class DbInvalidFormatIdError(ServerBaseException):
    def __init__(self, message="The Id is invalid, must be UUID 🆔") -> None:
        super().__init__(message)
        self.add_note("""
            El id que mandas no es el adecuado, debe ser un UUID.
        """)
        self.error_code = error_codes["DB_INVALID_FORMAT_ID"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class DataValidationError(ServerBaseException):
    def __init__(self, message="There are errors in the fields 🚫") -> None:
        super().__init__(message)
        self.add_note("""
            Alguno de los campos no tiene el tipo correcto.
        """)
        self.error_code = error_codes["ERROR_DATA_VALIDATION"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class ServerUnknownError(ServerBaseException):
    def __init__(self, message="Unknown error ❌", detail=None) -> None:
        super().__init__(message)
        self.add_note(f"""
            Hubo un error en el servidor. {detail}
        """)
        self.error_code = error_codes["SERVER_UNKNOWN_ERROR"]
        self.status_code = status_codes["INTERNAL_SERVER_ERROR"]
        self.http_argument = "Internal Server Error 💀"


class InvalidImageTypeError(ServerBaseException):
    def __init__(self, message="The image type is not valid 📸", detail=None) -> None:
        super().__init__(message)
        self.add_note(f"""
            Hubo un error al procesar la imagen. {detail}
        """)
        self.error_code = error_codes["ERROR_DATA_VALIDATION"]
        self.status_code = status_codes["UNSUPPORTED_MEDIA_TYPE"]
        self.http_argument = "Unsupported Media Type 💾"


class FilesNotFound(ServerBaseException):
    def __init__(self, message="File or directory not found 📂", detail=None) -> None:
        super().__init__(message)
        self.add_note(f"""
            No se encuentra el archivo o ruta. {detail}
        """)
        self.error_code = error_codes["FILE_NOT_FOUND"]
        self.status_code = status_codes["INTERNAL_SERVER_ERROR"]
        self.http_argument = "Internal Server Error 💀"


class PasswordDoNotMatchError(ServerBaseException):
    def __init__(self, message="Passwords do not match 🔐") -> None:
        super().__init__(message)
        self.add_note("""
            Las contraseñas no coinciden.
        """)
        self.error_code = error_codes["PASSWORD_DO_NOT_MATCH"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class ExpiredTokenError(ServerBaseException):
    def __init__(self, message="Token has expired 💨") -> None:
        super().__init__(message)
        self.add_note("""
            El token ha expirado.
        """)
        self.error_code = error_codes["EXPIRED_TOKEN"]
        self.status_code = status_codes["UNAUTHORIZED"]
        self.http_argument = "Unauthorized ⚠️"


class NotFoundTokenError(ServerBaseException):
    def __init__(self, message="Token not found 🤷‍♂️") -> None:
        super().__init__(message)
        self.add_note("""
            No se encuentra el token en el header.
        """)
        self.error_code = error_codes["NOT_FOUND_TOKEN"]
        self.status_code = status_codes["FORBIDDEN"]
        self.http_argument = "Forbidden ⚔️"


class InvalidTokenError(ServerBaseException):
    def __init__(self, message="The token is invalid 🔏") -> None:
        super().__init__(message)
        self.add_note("""
            El token es inválido.
        """)
        self.error_code = error_codes["INVALID_TOKEN"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class IncorrectUserError(ServerBaseException):
    def __init__(self, message="The token does not correspond to the user 🤡") -> None:
        super().__init__(message)
        self.add_note("""
            El token que mandas no corresponde con el usuario.
        """)
        self.error_code = error_codes["INCORRECT_USER"]
        self.status_code = status_codes["UNAUTHORIZED"]
        self.http_argument = "Unauthorized ⚠️"


class DuplicatedAppointmentError(ServerBaseException):
    def __init__(
            self,
            message="You cannot create two appointments at once, wait to complete one 🤡"
    ) -> None:
        super().__init__(message)
        self.add_note("""
            Hay una cita pendiente, no puedes hacer otra hasta completar la anterior.
        """)
        self.error_code = error_codes["DUPLICATED_APPOINTMENT"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"
        

class BusyAppointmentError(ServerBaseException):
    def __init__(
            self,
            message="There is already an appointment created for that time, please choose another time. 🤡"
    ) -> None:
        super().__init__(message)
        self.add_note("""
            Hay una cita con esa horario, elige otro.
        """)
        self.error_code = error_codes["BUSY_APPOINTMENT"]
        self.status_code = status_codes["BAD_REQUEST"]
        self.http_argument = "Bad Request ❓"


class EmailSenderError(ServerBaseException):

    def __init__(self, message="Error sending email 📨", detail=None) -> None:
        super().__init__(message)
        self.add_note(f"""
            Ocurrió un error al enviar el correo. {detail}
        """)
        self.error_code = error_codes["MAIL_NOT_SENT"]
        self.status_code = status_codes["INTERNAL_SERVER_ERROR"]
        self.http_argument = "Internal Server Error 💀"

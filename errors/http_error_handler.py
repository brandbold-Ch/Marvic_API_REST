from utils.status_codes import status_codes
from functools import wraps


class HandlerResponses:

    @staticmethod
    def __template(status: str, message: str, st_code: int, err_code: int, data: dict):
        return {
            "status": status,
            "message": message,
            "codes": {
                "status_code": st_code,
                "code_error": err_code
            },
            "data": data
        }

    @staticmethod
    def internal_server_error(message: str, err_code=None) -> dict:
        return HandlerResponses.__template(
            status="INTERNAL SERVER ERROR",
            message=message,
            st_code=status_codes["INTERNAL_SERVER_ERROR"],
            err_code=err_code,
            data={}
        )

    @staticmethod
    def ok(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="OK",
            message=message,
            st_code=200,
            err_code=err_code,
            data=data
        )

    @staticmethod
    def accepted(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="ACCEPTED",
            message=message,
            st_code=status_codes["ACCEPTED"],
            err_code=err_code,
            data=data
        )

    @staticmethod
    def created(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="CREATED",
            message=message,
            st_code=status_codes["CREATED"],
            err_code=err_code,
            data=data
        )

    @staticmethod
    def bad_request(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="BAD REQUEST",
            message=message,
            st_code=status_codes["BAD_REQUEST"],
            err_code=err_code,
            data=data
        )

    @staticmethod
    def unprocessable_entity(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="UNPROCESSABLE ENTITY",
            message=message,
            st_code=status_codes["UNPROCESSABLE_ENTITY"],
            err_code=err_code,
            data=data
        )

    @staticmethod
    def not_found(message, err_code=None, data=None) -> dict:
        return HandlerResponses.__template(
            status="NOT FOUND",
            message=message,
            st_code=status_codes["NOT_FOUND"],
            err_code=err_code,
            data=data
        )

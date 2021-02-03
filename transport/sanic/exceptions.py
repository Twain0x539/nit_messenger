from sanic.exceptions import SanicException


class SanicRequestValidationException(SanicException):
    status_code = 400


class SanicUserConflictException(SanicException):
    status_code = 409


class SanicResponseValidationException(SanicException):
    status_code = 500


class SanicPasswordHashException(SanicException):
    status_code = 500


class SanicDBException(SanicException):
    status_code = 500


class SanicAuthException(SanicException):
    status_code = 401


class SanicUserNotFoundException(SanicException):
    status_code = 404


class SanicCantGetUidFromTokenException(SanicException):
    status_code = 400


class SanicUserDontHaveAccessException(SanicException):
    status_code = 403


class SanicMessageDeletedException(SanicException):
    status_code = 403


class SanicMessageAlreadyDeletedException(SanicException):
    status_code = 409
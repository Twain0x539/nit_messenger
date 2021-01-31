from marshmallow import Schema, fields

from api.base import RequestDto

from helpers.validation import PasswordValidator


class RequestAuthUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False, validate=PasswordValidator.params())


class RequestAuthUserDto(RequestDto, RequestAuthUserDtoSchema):
    __schema__ = RequestAuthUserDtoSchema
from marshmallow import Schema, fields, validate

from api.base import RequestDto
from helpers.validation import LoginValidator, PasswordValidator, NameValidator


class RequestCreateUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False, validate=LoginValidator.params())
    password = fields.Str(required=True, allow_none=False, validate=PasswordValidator.params())
    first_name = fields.Str(required=True, allow_none=False, validate=NameValidator.params())
    last_name = fields.Str(required=True, allow_none=False, validate=NameValidator.params())


class RequestCreateUserDto(RequestDto, RequestCreateUserDtoSchema):
    __schema__ = RequestCreateUserDtoSchema



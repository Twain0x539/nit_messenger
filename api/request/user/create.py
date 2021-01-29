from marshmallow import Schema, fields, validate

from api.base import RequestDto
from helpers.validation import Validator

class RequestCreateUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)

class RequestCreateUserDto(RequestDto, RequestCreateUserDtoSchema):
    __schema__ = RequestCreateUserDtoSchema



    #validate = (validate.Regexp(regex=r"[a-zA-Z0-9_\-]*$",
    #error="User name must not contain special characters", ), validate.Length(1))
    #)
    #Validator(type=RegexNoSpecialSymbols, min_length=5))
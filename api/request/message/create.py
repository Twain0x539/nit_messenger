from marshmallow import Schema, fields

from api.base import RequestDto

from helpers.validation import LoginValidator

class RequestCreateMessageDtoSchema(Schema):
    message = fields.Str(required=True, allow_none=False)
    recipient = fields.Str(required=True, allow_none=False, validate=LoginValidator.params())


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema
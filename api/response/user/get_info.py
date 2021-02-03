from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseGetUserDtoSchema(Schema):
    id = fields.Int(required=True, allow_none=False)
    login = fields.Str(required=True, allow_none=False)
    created_at = fields.Str(required=True, allow_none=False)
    updated_at = fields.Str(allow_none=True)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)


class ResponseGetUserDto(ResponseDto, ResponseGetUserDtoSchema):
    __schema__ = ResponseGetUserDtoSchema

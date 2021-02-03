from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseGetMessageInfoDtoSchema(Schema):
    id = fields.Int(required=True, allow_none=False)
    sender_id = fields.Int(required=True, allow_none=False)
    recipient_id = fields.Int(required=True, allow_none=False)
    created_at = fields.Str(required=True, allow_none=False)
    updated_at = fields.Str(required=True, allow_none=True)
    message = fields.Str(required=True, allow_none=False)


class ResponseGetMessageInfoDto(ResponseDto, ResponseGetMessageInfoDtoSchema):
    __schema__ = ResponseGetMessageInfoDtoSchema

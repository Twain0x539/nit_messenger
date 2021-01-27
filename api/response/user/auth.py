from marshmallow import Schema, fields
from api.base import ResponseDto

class ResponseAuthUserDtoSchema(Schema):
    Authorization = fields.Str(allow_none=False, required=True)

class ResponseAuthUserDto(ResponseDto, ResponseAuthUserDtoSchema):
    __schema__ = ResponseAuthUserDtoSchema

class AuthResponseObject:
    def __init__(self, token):
        self.Authorization = token

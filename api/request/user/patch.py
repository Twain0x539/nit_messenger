from marshmallow import Schema, fields

from api.base import RequestDto

from helpers.validation import NameValidator

class RequestPatchUserDtoSchema(Schema):
    first_name = fields.Str(validate=NameValidator.params())
    last_name = fields.Str(validate=NameValidator.params())

class RequestPatchUserDto(RequestDto,RequestPatchUserDtoSchema):
    fields: list
    __schema__ = RequestPatchUserDtoSchema

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestPatchUserDto, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(RequestPatchUserDto, self).set(key, value)

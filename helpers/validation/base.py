from marshmallow import validate


class Validator:
    regexp: str
    length: int
    match_error: str

    @classmethod
    def params(cls):
        return (validate.Regexp(cls.regexp, error=cls.match_error), validate.Length(cls.length))



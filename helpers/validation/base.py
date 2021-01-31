from marshmallow import validate


class Validator():
    regexp: str
    length: int
    match_error: str

    @classmethod
    def params(self):
        return (validate.Regexp(self.regexp, error=self.match_error), validate.Length(self.length))

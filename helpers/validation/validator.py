from marshmallow.validate import Regexp, Length

class Validator():
    def __init__(self, type, min_length):
        self.type = type
        self.min_length = min_length

    def __get__(self,instance, owner):
        return None
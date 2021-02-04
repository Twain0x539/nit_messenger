from helpers.validation.base import Validator


class LoginValidator(Validator):
    regexp = r"[a-zA-Z0-9_\-]*$"
    length = 1
    match_error = "Login must not contain special symbols and spaces"


class PasswordValidator(Validator):
    regexp = r"[a-zA-Z0-9_\-]*$"
    length = 1
    match_error = "Password must not contain special symbols and spaces"


class NameValidator(Validator):
    regexp = r"[a-zA-Z\-\s]*$"
    length = 1
    match_error = "Name must not contain special symbols and numbers"

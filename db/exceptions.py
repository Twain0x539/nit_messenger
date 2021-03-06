class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserExistsException(Exception):
    pass


class DBUserNotExistsException(Exception):
    pass


class DBNotYourMessageException(Exception):
    pass


class DBMessageNotExistsException(Exception):
    pass


class DBMessageDeletedException(Exception):
    pass

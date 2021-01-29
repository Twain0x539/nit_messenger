from datetime import datetime

from db.database import DBSession
from db.models import DBUser
from db.exceptions import DBUserExistsException, DBUserNotExistsException


from api.request.user import RequestCreateUserDto
from api.request.user import RequestPatchUserDto


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at = datetime.now(),
        updated_at = None,
    )
    if session.get_user_by_login(new_user.login) is not None:
        raise DBUserExistsException

    session.add_model(new_user)

    return new_user


def get_user(session: DBSession, *, login: str = None, uid: int = None) -> DBUser:
    db_user = None
    if login is not None:
        db_user = session.get_user_by_login(login)
    elif uid is not None:
        db_user = session.get_user_by_id(uid)

    if db_user is None:
        raise DBUserNotExistsException
    return db_user

def patch_user(session: DBSession, user: RequestPatchUserDto, uid: int) -> DBUser:
    db_user = session.get_user_by_id(uid)
    for attr in user.fields:
        if hasattr(user, attr):
            value = getattr(user, attr)
            setattr(db_user, attr, value)
    db_user.updated_at = datetime.now()

    return db_user
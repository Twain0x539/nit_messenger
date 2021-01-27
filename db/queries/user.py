from datetime import datetime

from db.database import DBSession
from db.models import DBUser
from db.exceptions import DBUserExistsException


from api.request.user.create import RequestCreateUserDto


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at = datetime.now(),
        update_at = None,
    )
    if session.get_user_by_login(new_user.login) is not None:
        raise DBUserExistsException

    session.add_model(new_user)

    return new_user

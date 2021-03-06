from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session, Query

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()

    def users(self) -> Query:
        return self.query(DBUser)

    def messages(self) -> Query:
        return self.query(DBMessage)

    def get_user_by_login(self, login: str) -> DBUser:
        return self.users().filter(DBUser.login == login).first()

    def get_user_by_id(self, uid: int) -> DBUser:
        try:
            return self.users().get(uid)
        except AttributeError:
            raise DBDataException

    def get_user_messages(self, uid: int):
        return self.messages().filter(DBMessage.recipient_id == uid).filter(DBMessage.is_deleted == 0)

    def get_message_by_id(self, msgid: int):
        try:
            return self.messages().get(msgid)
        except AttributeError:
            raise DBDataException


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)

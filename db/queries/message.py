from datetime import datetime

from db.database import DBSession
from db.models.message import DBMessage
from db.queries import user as user_queries
from db.exceptions import DBNotYourMessageException, DBMessageNotExistsException, DBMessageDeletedException

from api.request.message import RequestCreateMessageDto, RequestPatchMessageDto


def create_message(session: DBSession, message: RequestCreateMessageDto, *, sender_id: int) -> DBMessage:

    new_message = DBMessage(
        message=message.message,
        sender_id=sender_id,
        recipient_id=user_queries.get_user(session, login=message.recipient).id,
        created_at=datetime.now(),
        updated_at=None,
        is_deleted=False,
    )

    session.add_model(new_message)

    return new_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, *, msgid: int, uid: int) -> DBMessage:
    db_message = session.get_message_by_id(msgid)

    if db_message is None or db_message.sender_id != uid:
        raise DBNotYourMessageException("You don't have access to this message")

    if db_message.is_deleted:
        raise DBMessageDeletedException

    db_message.message = message.message
    db_message.updated_at = datetime.now()
    return db_message


def get_user_messages(session: DBSession, *, uid: int) -> tuple[DBMessage]:
    return session.get_user_messages(uid)


def get_message_by_id(session: DBSession, *, msgid: int, uid: int) -> DBMessage:
    db_message = session.get_message_by_id(msgid)
    if db_message is None or (db_message.sender_id != uid and db_message.recipient_id != uid):
        raise DBNotYourMessageException("You don't have access to this message")

    if db_message.is_deleted:
        raise DBMessageDeletedException

    return db_message


def delete_message(session: DBSession, *, msgid: int, uid: int) -> DBMessage:

    db_message = session.get_message_by_id(msgid)

    if db_message is None or db_message.sender_id != uid:
        raise DBNotYourMessageException("You don't have access to this message")

    if db_message.is_deleted:
        raise DBMessageDeletedException
    print(db_message.is_deleted)
    db_message.is_deleted = 1
    print(db_message.is_deleted)
    db_message.updated_at = datetime.now()

    return db_message

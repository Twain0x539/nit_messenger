from datetime import datetime

from db.database import DBSession
from db.models.message import DBMessage
from db.queries import user as user_queries
from db.exceptions import DBNotYourMessageException, DBMessageNotExistsException, DBMessageDeletedException

from api.request.message import RequestCreateMessageDto, RequestPatchMessageDto


def create_message(session: DBSession, message: RequestCreateMessageDto, *, sender_id: int):

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


def patch_message(session: DBSession, message: RequestPatchMessageDto, msgid: int, sender_id: int,):
    db_message = session.get_message_by_id(msgid)
    if message is None:
        raise DBMessageNotExistsException
    if db_message.sender_id != sender_id:
        raise DBNotYourMessageException
    else:
        message.message = message
        return db_message


def get_user_messages(session: DBSession, uid: int):
    return session.get_user_messages(uid)


def get_message_by_id(session: DBSession, msgid: int, uid: int):
    message = session.get_message_by_id(msgid)
    if message is None:
        raise DBMessageNotExistsException
    if message.is_deleted:
        raise DBMessageDeletedException
    if message.recipient_id == uid or message.sender_id == uid:
        return message
    else:
        raise DBNotYourMessageException("You don't have access to this message")


def delete_message_by_id(session: DBSession, msgid: int, uid: int):
    message = session.get_message_by_id(msgid)
    if message is None:
        raise DBMessageNotExistsException
    if message.is_deleted:
        raise DBMessageDeletedException
    if message.sender_id == uid:
        message.is_deleted = True
        return message
    else:
        raise DBNotYourMessageException("You don't have access to this message")
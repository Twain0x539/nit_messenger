from datetime import datetime

from db.database import DBSession
from db.models.message import DBMessage
from db.queries import user as user_queries
from db.exceptions import DBNotYourMessageException, DBMessageNotExistsException

from api.request.message import RequestCreateMessageDto


def create_message(session: DBSession, message: RequestCreateMessageDto, *, sender_id: int,):

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


def get_user_messages(session: DBSession, uid: int):
    return session.get_user_messages(uid)


def get_message_by_id(session: DBSession, msgid: int, uid: int):
    message = session.get_message_by_id(msgid)
    if message is None:
        raise DBMessageNotExistsException
    if message.recipient_id == uid or message.sender_id == uid:
        return session.get_message_by_id(msgid)
    else:
        raise DBNotYourMessageException("You don't have access to this message")
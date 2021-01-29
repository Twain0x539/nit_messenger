from datetime import datetime

from db.database import DBSession
from db.models.message import DBMessage
from db.queries import user as user_queries

from api.request.message import RequestCreateMessageDto


def create_message(session: DBSession, message: RequestCreateMessageDto, *, sender_id: int,):

    new_message = DBMessage(
        message=message.message,
        sender_id=sender_id,
        recipient_id=user_queries.get_user(session, login=message.recipient).id,
        created_at=datetime.now(),
        updated_at=None,
    )

    session.add_model(new_message)

    return new_message


def get_user_messages(session: DBSession, uid: int):
    return session.get_user_messages(uid)
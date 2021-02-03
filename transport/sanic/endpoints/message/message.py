from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicCantGetUidFromTokenException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBIntegrityException, DBDataException

from api.request.message import RequestCreateMessageDto
from api.response.message import ResponseGetMessageInfoDto


class MessageEndpoint(BaseEndpoint):


    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            uid = token['uid']
        except KeyError:
            raise SanicCantGetUidFromTokenException("Can't get uid from token")

        db_messages = message_queries.get_user_messages(session, uid=token['uid'])

        response_model = ResponseGetMessageInfoDto(db_messages, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())


    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            uid = token['uid']
        except KeyError:
            raise SanicCantGetUidFromTokenException("Can't get uid from token")

        db_new_msg = message_queries.create_message(session, message=request_model, sender_id=uid)

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseGetMessageInfoDto(db_new_msg)

        return await self.make_response_json(status=201, body=response_model.dump())





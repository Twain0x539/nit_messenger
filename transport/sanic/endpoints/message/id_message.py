from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message import RequestPatchMessageDto
from api.response.message import ResponseGetMessageInfoDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserDontHaveAccessToMessageException, SanicMessageDeletedException
from transport.sanic.exceptions import SanicDBException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBNotYourMessageException, DBMessageNotExistsException, DBMessageDeletedException
from db.exceptions import DBDataException, DBIntegrityException


class IdentifiedMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, msgid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            db_message = message_queries.get_message_by_id(session, msgid=msgid, uid=token['uid'])
        except (DBNotYourMessageException, DBMessageNotExistsException):
            raise SanicUserDontHaveAccessToMessageException("You can't view that message")
        except DBMessageDeletedException:
            raise SanicMessageDeletedException("This message was deleted!")

        response_model = ResponseGetMessageInfoDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())


    async def method_delete(
            self, request: Request, body: dict, session: DBSession, msgid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        try:
            uid = token['uid']
        except KeyError:
            return await self.make_response_json(status=400, message="Can't get uid from token")

        try:
            db_message = message_queries.delete_message(session, msgid=msgid, uid=uid)
        except (DBNotYourMessageException, DBMessageNotExistsException) as e:
            raise SanicUserDontHaveAccessToMessageException("You can't view that message")
        except DBMessageDeletedException:
            raise SanicMessageDeletedException("Message already deleted")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=201, body={})


    async def method_patch(
            self, request: Request, body: dict, session: DBSession, msgid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            uid = token['uid']
        except KeyError:
            return await self.make_response_json(status=400, message="Can't get uid from token")

        request_model = RequestPatchMessageDto(body)

        try:
            db_patched_message = message_queries.patch_message(session, request_model, msgid=msgid, uid=uid)
        except (DBNotYourMessageException, DBMessageNotExistsException) as e:
            raise SanicUserDontHaveAccessToMessageException("You don't have access to this message")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseGetMessageInfoDto(db_patched_message)

        return await self.make_response_json(status=201, body=response_model.dump())

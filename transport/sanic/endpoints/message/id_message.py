from sanic.request import Request

from api.response.message import ResponseGetMessageInfoDto

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserDontHaveAccessToMessage, SanicMessageDeletedException

from db.database import DBSession
from db.queries import message as message_queries
from db.exceptions import DBNotYourMessageException, DBMessageNotExistsException, DBMessageDeletedException

class IdentifiedMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, msgid: int, token: dict, *args, **kwargs
    ):
        try:
            db_message = message_queries.get_message_by_id(session, msgid, token['uid'])
        except (DBNotYourMessageException, DBMessageNotExistsException):
            raise SanicUserDontHaveAccessToMessage("You can't view that message")
        except DBMessageDeletedException:
            raise SanicMessageDeletedException("This message was deleted!")

        response_model = ResponseGetMessageInfoDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, msgid: int, token: dict, *args, **kwargs
    ):
        try:
            db_message = message_queries.get_message_by_id(session, msgid, token['uid'])
        except (DBNotYourMessageException, DBMessageNotExistsException) as e:
            raise SanicUserDontHaveAccessToMessage("You can't view that message")

        response = {}

        return await self.make_response_json(status=200, body=response.dump())

    async def method_patch(self):
        pass
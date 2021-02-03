from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserNotFoundException, SanicUserDontHaveAccessException
from transport.sanic.exceptions import SanicCantGetUidFromTokenException

from db.queries import user as user_queries
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException, DBUserNotExistsException

from api.response.user import ResponseGetUserDto
from api.request.user import RequestPatchUserDto


class UserEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            requested_user = token['uid']
        except KeyError:
            raise SanicCantGetUidFromTokenException("Can't get uid from token")

        if uid != requested_user:
            raise SanicUserDontHaveAccessException("Insufficient permission")

        try:
            db_user = user_queries.get_user(session=session, uid=uid)
        except (DBDataException, DBIntegrityException):
            raise SanicDBException("Database exception")
        except DBUserNotExistsException:
            raise SanicUserNotFoundException('User not found')

        response_model = ResponseGetUserDto(db_user)
        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchUserDto(body)

        try:
            requested_user = token['uid']
        except KeyError:
            raise SanicCantGetUidFromTokenException("Can't get uid from token")

        if uid != requested_user:
            raise SanicUserDontHaveAccessException("Insufficient permission")

        try:
            db_user = user_queries.patch_user(session, request_model, uid=uid)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseGetUserDto(db_user)
        return await self.make_response_json(status=200, body=response_model.dump())



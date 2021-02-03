from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicPasswordHashException, SanicDBException
from transport.sanic.exceptions import SanicUserNotFound

from db.database import DBSession
from db.queries import user as user_queries
from db.exceptions import DBDataException, DBIntegrityException, DBUserNotExistsException

from api.request.user.auth import RequestAuthUserDto
from api.response.user.auth import ResponseAuthUserDto, AuthResponseObject

from helpers.password.hash import check_hash
from helpers.password.exception import CheckPasswordHashException
from helpers.auth.token import create_token


class AuthUserEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestAuthUserDto(body)

        try:
            db_user = user_queries.get_user(session, login=request_model.login)
        except DBUserNotExistsException:
            raise SanicUserNotFound('User not found')
        except (DBDataException, DBIntegrityException):
            raise SanicDBException('Database error')

        try:
            check_hash(request_model.password, db_user.password)
        except CheckPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'uid': db_user.id,
        }

        token = create_token(payload)
        response = AuthResponseObject(token)
        response_model = ResponseAuthUserDto(response)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )



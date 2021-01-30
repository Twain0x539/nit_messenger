from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicPasswordHashException, SanicUserConflictException, SanicDBException

from db.database import DBSession
from db.queries import user as user_queries
from db.exceptions import DBUserExistsException, DBDataException, DBIntegrityException

from api.request.user.create import RequestCreateUserDto
from api.response.user.get_info import ResponseGetUserDto

from helpers.password.hash import generate_hash
from helpers.password.exception import GeneratePasswordHashException



class CreateUserEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestCreateUserDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as e:
            raise SanicPasswordHashException(str(e))


        try:
            db_new_user = user_queries.create_user(session, request_model, hashed_password)
        except DBUserExistsException:
            raise SanicUserConflictException('Login is busy')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseGetUserDto(db_new_user)

        return await self.make_response_json(body=response_model.dump(), status=201)



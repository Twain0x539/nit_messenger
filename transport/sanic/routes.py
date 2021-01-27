from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST'),
        ),
        endpoints.CreateUserEndpoint(
            config=config, context=context, uri='/user', methods=('POST',),
        ),

        endpoints.AuthUserEndpoint(
            config=config, context=context, uri='/auth', methods=('POST',),
        ),
    )
"""
        endpoints.UserEndpoint(
            config=config, context=context, uri='/user/<uid:int>', methods=('GET', 'POST'),
        ),
        endpoints.MessageEndpoint(
            config=config, context=context, uri='/msg', methods=('GET', 'POST'),
        ),
        endpoints.IdentifiedMessageEndpoint(
            config=config, context=context, uri='/msg/<uid:int>', methods=('GET', 'DELETE', "PATCH")
        ),
"""
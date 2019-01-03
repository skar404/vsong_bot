from sanic import Sanic
from aiohttp import ClientSession
from aiopg.sa import Engine
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger

from app.web import bp


class SanicApp(Sanic):
    aiohttp_session: ClientSession
    pg_client: Engine


application = SanicApp(__name__, log_config=LOGGING_CONFIG_DEFAULTS)


def run_web():
    @application.listener('before_server_start')
    async def init(app: SanicApp, loop):
        app.aiohttp_session = ClientSession(loop=loop)

    @application.listener('after_server_stop')
    def finish(app, loop):
        loop.run_until_complete(app.session.close())
        loop.close()

    application.blueprint(bp)

    application.go_fast(debug=True)

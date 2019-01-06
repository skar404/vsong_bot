import aiohttp
from sanic import Sanic
from aiohttp import ClientSession
from aiopg.sa import Engine
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger

from app import settings
from app.clients.Telegram import TelegramSDK
from app.web import bp, bot_handler


class SanicApp(Sanic):
    aiohttp_session: ClientSession
    pg_client: Engine


application = SanicApp(__name__, log_config=LOGGING_CONFIG_DEFAULTS)


def create_app(app: SanicApp) -> SanicApp:
    @app.listener('before_server_start')
    async def init(app: SanicApp, loop):
        app.aiohttp_session = ClientSession(loop=loop, connector=aiohttp.TCPConnector(verify_ssl=False))

        # update telegram web hook
        assert (await TelegramSDK().update_web_hook()).get('ok')

    @app.listener('after_server_stop')
    async def finish(app, loop):
        loop.run_until_complete(app.session.close())
        loop.close()

    app.blueprint(bp)
    bot_handler.register()

    return app


def run_web():
    create_app(application).go_fast(
        debug=settings.DEBUG,
        workers=settings.WORKERS_NUM,
        auto_reload=False  # если включить то сломаеться дебаг в PyCharm
    )

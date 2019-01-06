import aiohttp
import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration
from sanic import Sanic
from aiohttp import ClientSession
from aiopg.sa import Engine, create_engine
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger

from app import settings
from app.clients.Telegram import TelegramSDK
from app.settings import PSQL_USER, PSQL_PASSWORD, PSQL_HOST, PSQL_POST, PSQL_DATE_BASE, SENTRY_KEY
from app.web import bp, bot_handler


class SanicApp(Sanic):
    aiohttp_session: ClientSession
    pg_client: Engine


sentry_sdk.init(
    dsn=SENTRY_KEY,
    integrations=[SanicIntegration()]
)

application = SanicApp(__name__, log_config=LOGGING_CONFIG_DEFAULTS)


def create_app(app: SanicApp) -> SanicApp:
    @app.listener('before_server_start')
    async def init(app: SanicApp, loop):
        app.aiohttp_session = ClientSession(loop=loop, connector=aiohttp.TCPConnector(verify_ssl=False))
        logger.info('init aiohttp_session')

        app.pg_client = await create_engine(
            user=PSQL_USER,
            password=PSQL_PASSWORD,
            host=PSQL_HOST,
            port=PSQL_POST,
            database=PSQL_DATE_BASE,
        )
        logger.info('init pg_client')

        # update telegram web hook
        assert (await TelegramSDK().update_web_hook()).get('ok')
        logger.info('init update_web_hook')

    @app.listener('after_server_stop')
    async def finish(app, loop):
        app.pg_client.close()
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

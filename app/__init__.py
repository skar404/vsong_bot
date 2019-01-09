from asyncio import ensure_future

import aio_pika
import aiobotocore
import aiohttp
import sentry_sdk
import vk_api
from aiobotocore import AioSession
from sentry_sdk.integrations.sanic import SanicIntegration
from sanic import Sanic
from aiohttp import ClientSession
from aiopg.sa import Engine, create_engine
from sanic.log import LOGGING_CONFIG_DEFAULTS, logger
from vk_api import VkApi

from app import settings
from app.clients.Telegram import TelegramSDK
from app.consume import consumers_init
from app.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_POST, POSTGRES_DB, SENTRY_KEY, RABBITMQ_HOST, \
    RABBITMQ_PORT, RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_VHOST, RABBITMQ_SSL, RABBITMQ_QUERY, RABBITMQ_EXCHANGE, \
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_END_POINT_URL, AWS_REGION_NAME, VK_LOGIN, VK_PASSWORD, VK_APP_ID, \
    PROXY_USER, PROXY_PASSWORD, PROXY_IP, PROXY_PORT
from app.web import bp, bot_handler


class SanicApp(Sanic):
    aio_pika: aio_pika.Connection
    aiohttp_session: ClientSession
    pg_client: Engine
    botocore_client: AioSession
    vk_session: VkApi

sentry_sdk.init(
    dsn=SENTRY_KEY,
    integrations=[SanicIntegration()]
)

application = SanicApp(__name__, log_config=LOGGING_CONFIG_DEFAULTS)


def create_app(app: SanicApp, web=False, consumer=False) -> SanicApp:
    @app.listener('before_server_start')
    async def init(app: SanicApp, loop):
        proxy_full_url = "{}:{}@{}:{}".format(
            PROXY_USER, PROXY_PASSWORD, PROXY_IP, PROXY_PORT
        )

        app.vk_session = vk_api.VkApi(
            login=VK_LOGIN,
            password=VK_PASSWORD,
            app_id=VK_APP_ID
        )
        app.vk_session.http.proxies = {
            'http': 'http://{}/'.format(proxy_full_url),
            'https': 'https://{}/'.format(proxy_full_url),
        }

        app.vk_session.auth()

        app.botocore_client = aiobotocore.get_session().create_client(
            service_name='s3',
            region_name=AWS_REGION_NAME,
            endpoint_url=AWS_END_POINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            verify=False
        )

        app.aio_pika = await aio_pika.connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_DEFAULT_USER,
            password=RABBITMQ_DEFAULT_PASS,
            virtualhost=RABBITMQ_DEFAULT_VHOST,
            ssl=RABBITMQ_SSL,
            loop=loop
        )

        channel = await app.aio_pika.channel()
        exchange = await channel.declare_exchange(RABBITMQ_EXCHANGE)

        # Declaring queue
        queue = await channel.declare_queue(RABBITMQ_QUERY, durable=True)

        # Binding queue
        await queue.bind(exchange, RABBITMQ_QUERY)

        app.aiohttp_session = ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        logger.info('init aiohttp_session')

        app.pg_client = await create_engine(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_POST,
            database=POSTGRES_DB,
        )
        logger.info('init pg_client')

        # Не критично, но количество запросов зависит от WORKERS_NUM
        req = (await TelegramSDK().update_web_hook()).get('ok')
        logger.info('init update_web_hook status {}'.format(req))

    if consumer:
        @app.listener('before_server_start')
        async def run_consumer(app: SanicApp, loop):
            ensure_future(consumers_init(app))

    if web:
        app.blueprint(bp)
        bot_handler.register()
    return app


def run_web():
    print(settings.SANIC_HOST)
    create_app(application, web=True, consumer=True).go_fast(
        debug=settings.DEBUG,
        workers=settings.WORKERS_NUM,
        host=settings.SANIC_HOST,
        auto_reload=False  # если включить то сломаеться дебаг в PyCharm
    )

import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


DEBUG = env('DEBUG', cast=bool, default=True)
WORKERS_NUM = env('WORKERS_NUM', cast=int, default=1)

BOT_SECRET_URL = env('BOT_SECRET_URL', default='test')
BOT_TOKEN = env('BOT_TOKEN', default='token')

BOT_WEB_HOOK = env('BOT_WEB_HOOK', default='https://test.ngrok.io/bot/{secret_url}').format(
    secret_url=BOT_SECRET_URL
)

PSQL_USER = env('PSQL_USER', default='postgres')
PSQL_PASSWORD = env('PSQL_PASSWORD', default='1234')
PSQL_HOST = env('PSQL_HOST', default='127.0.0.1')
PSQL_POST = env('PSQL_POST', cast=int, default=5432)
PSQL_DATE_BASE = env('PSQL_DATE_BASE', default='dev')

SENTRY_KEY = env('SENTRY_KEY', default='')

RABBIT_HOST = env('RABBIT_HOST', default='127.0.0.1')
RABBIT_PORT = env('RABBIT_PORT', cast=int, default=5672)
RABBIT_USER = env('RABBIT_USER', default='rebbitmq')
RABBIT_PASSWORD = env('RABBIT_PASSWORD', default='1234')
RABBIT_VHOST = env('RABBIT_VHOST', default='dev_vhost')
RABBIT_SSL = env('RABBIT_SSL', cast=bool, default=False)

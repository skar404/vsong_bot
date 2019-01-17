import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


DEBUG = env('DEBUG', cast=bool, default=True)
SANIC_HOST = env('SANIC_HOST', cast=str, default='0.0.0.0')
WORKERS_NUM = env('WORKERS_NUM', cast=int, default=1)

BOT_SECRET_URL = env('BOT_SECRET_URL', default='test')
BOT_TOKEN = env('BOT_TOKEN', default='token')

BOT_WEB_HOOK = env('BOT_WEB_HOOK', default='https://test.ngrok.io/bot/{secret_url}').format(
    secret_url=BOT_SECRET_URL
)

POSTGRES_USER = env('POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default='1234')
POSTGRES_HOST = env('POSTGRES_HOST', default='127.0.0.1')
POSTGRES_POST = env('POSTGRES_POST', cast=int, default=5432)
POSTGRES_DB = env('POSTGRES_DB', default='dev')

SENTRY_KEY = env('SENTRY_KEY', default='')

RABBITMQ_HOST = env('RABBITMQ_HOST', default='127.0.0.1')
RABBITMQ_PORT = env('RABBITMQ_PORT', cast=int, default=5672)
RABBITMQ_DEFAULT_USER = env('RABBITMQ_DEFAULT_USER', default='rebbitmq')
RABBITMQ_DEFAULT_PASS = env('RABBITMQ_DEFAULT_PASS', default='1234')
RABBITMQ_DEFAULT_VHOST = env('RABBITMQ_DEFAULT_VHOST', default='dev_vhost')
RABBITMQ_SSL = env('RABBITMQ_SSL', cast=bool, default=False)
RABBITMQ_QUERY = env('RABBITMQ_QUERY', default='song_list')
RABBITMQ_EXCHANGE = env('RABBITMQ_EXCHANGE', default='bot.message')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_END_POINT_URL = env('AWS_END_POINT_URL', default='')
AWS_REGION_NAME = env('AWS_REGION_NAME', default='')
AWS_BUCKET = env('AWS_BUCKET', default='tmp')

VK_LOGIN = env('VK_LOGIN', default='')
VK_PASSWORD = env('VK_PASSWORD', default='')

VK_APP_ID = env('VK_APP_ID', default='')

PROXY_USER = env('PROXY_USER', default='')
PROXY_PASSWORD = env('PROXY_PASSWORD', default='')
PROXY_IP = env('PROXY_IP', default='')
PROXY_PORT = env('PROXY_PORT', cast=int, default=8080)

import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_envfile(os.path.join(BASE_DIR, '.env'))


DEBUG = env('DEBUG', cast=bool, default=True)
WORKERS_NUM = env('WORKERS_NUM', cast=int, default=1)

BOT_SECRET_URL = env('BOT_SECRET_URL', cast=str, default='test')
BOT_TOKEN = env('BOT_TOKEN', cast=str, default='token')

BOT_WEB_HOOK = env('BOT_WEB_HOOK', cast=str, default='https://test.ngrok.io/bot/{secret_url}').format(
    secret_url=BOT_SECRET_URL
)

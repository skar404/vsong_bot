import os

from envparse import Env

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

env = Env()
env.read_envfile()

BOT_TOKEN = env.str('BOT_TOKEN')
BOT_WEB_HOOK = env.str('BOT_WEB_HOOK')

VK_APP_ID = env.str('VK_APP_ID')
VK_LOGIN = env.str('VK_LOGIN')
VK_PASSWORD = env.str('VK_PASSWORD')

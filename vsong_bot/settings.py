import os
from dataclasses import dataclass

from envparse import Env

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

env = Env()
env.read_envfile()


@dataclass
class RabbitConnectInfo:
    login: str
    password: str
    host: str
    port: int
    virtual_host: str

    def make_rabbit_url(self) -> str:
        return f'amqp://{self.login}:{self.password}@{self.host}:{self.port}/{self.virtual_host}'


BOT_TOKEN = env.str('BOT_TOKEN')
BOT_WEB_HOOK = env.str('BOT_WEB_HOOK')

VK_APP_ID = env.str('VK_APP_ID')
VK_LOGIN = env.str('VK_LOGIN')
VK_PASSWORD = env.str('VK_PASSWORD')

RABBIT_MQ = RabbitConnectInfo(
    login=env.str('RABBIT_LOGIN', default='guest'),
    password=env.str('RABBIT_PASSWORD', default='guest'),
    host=env.str('RABBIT_HOST', default='localhost'),
    port=env.int('RABBIT_PORT', default='5672'),
    virtual_host=env.str('RABBIT_VIRTUAL_HOST', default='dev_vhost')
)

RABBIT_MQ_URL = RABBIT_MQ.make_rabbit_url()

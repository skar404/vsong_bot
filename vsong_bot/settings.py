import os

from envparse import Env

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

env = Env()
env.read_envfile()

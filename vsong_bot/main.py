from aiohttp import web

from vsong_bot.consumers.consumer import run
from vsong_bot.consumers.download_song import DownloadSongConsumer
from vsong_bot.consumers.update_song import UpdateSongConsumer
from vsong_bot.routes import setup_routes
from vsong_bot.settings import RABBIT_MQ_URL


def run_api():
    app = web.Application()
    setup_routes(app)
    web.run_app(app)


def run_consumer():
    run([
        DownloadSongConsumer(RABBIT_MQ_URL),
        UpdateSongConsumer(RABBIT_MQ_URL)
    ])

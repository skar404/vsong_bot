from aiohttp import web

from vsong_bot.routes import setup_routes


async def init_app():
    app = web.Application()
    setup_routes(app)

    return app


def run_api():
    app = init_app()
    web.run_app(app)

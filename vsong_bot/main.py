import asyncio

import aio_pika
from aiohttp import web

from vsong_bot.routes import setup_routes
from vsong_bot.settings import RABBIT_MQ_URL


async def init_api():
    app = web.Application()
    setup_routes(app)

    return app


def run_api():
    app = init_api()
    web.run_app(app)


async def init_consumer(loop):
    connection = await aio_pika.connect_robust(RABBIT_MQ_URL, loop=loop)

    async with connection:
        queue_name = "test_queue"

        # Creating channel
        channel = await connection.channel()    # type: aio_pika.Channel

        # Declaring queue
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )   # type: aio_pika.Queue

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break


def run_consumer():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_consumer(loop))
    loop.close()

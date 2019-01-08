import json

from sanic.log import logger

from app.settings import RABBIT_QUERY


async def download_song(message):
    logger.info('start consumer download_song')
    with message.process():
        message_body = json.loads(message.body)


async def consumer_download_song(app):
    queue_name = RABBIT_QUERY

    # Creating channel
    channel = await app.aio_pika.channel()

    # Declaring queue
    queue = await channel.declare_queue(
        queue_name,
        durable=True,
    )

    await queue.consume(download_song)

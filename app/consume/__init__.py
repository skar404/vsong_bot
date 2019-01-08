import json

from sanic.log import logger

from app import TelegramSDK
from app.bot.handler import RabbitMessageType
from app.settings import RABBIT_QUERY


async def download_song(message):
    await TelegramSDK().send_message(chat_id=message['chat_id'], message='Вот ваш трек: {}'.format(
        message['text']
    ))
    await TelegramSDK().delete_message(chat_id=message['chat_id'], message_id=message['message_id'])


SWITCH = {
    RabbitMessageType.DOWNLOAD_SONG: download_song
}


async def consumer_bot_message(message):
    logger.info('start consumer download_song')
    with message.process():
        message_body = json.loads(message.body)

        await SWITCH[message_body['type']](message_body)


async def consumers_init(app):
    queue_name = RABBIT_QUERY

    # Creating channel
    channel = await app.aio_pika.channel()

    # Declaring queue
    queue = await channel.declare_queue(
        queue_name,
        durable=True,
    )

    await queue.consume(consumer_bot_message)

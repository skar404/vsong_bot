import json

from sanic.log import logger
from vk_api.audio import VkAudio

from app.clients.Telegram import TelegramSDK
from app.bot.handler import RabbitMessageType
from app.models import MusicModel
from app.settings import RABBITMQ_QUERY


async def get_vk_song_list(song_text):
    from app import application

    vk_audio = VkAudio(application.vk_session)
    return [{
        'artist': song.get('artist'),
        'title': song.get('title'),
        'duration': song.get('duration'),
        'v_url': song.get('url'),
        'vk_id': song.get('id'),
        'owner_id': song.get('owner_id'),
    } for song in vk_audio.search(q=song_text)]


def get_song_text(song_list):
    return '\n'.join([f'{i}. {song["artist"]} - {song["title"]} ({song["duration"]})\n/song\_{song["id"]}'
                      for i, song in enumerate(song_list)])


async def download_song(message):
    from app import application

    song_list = await get_vk_song_list(message['text'])

    smtp = MusicModel.__table__.insert().values(song_list).returning(*MusicModel.__table__.c)
    async with application.pg_client.acquire() as conn:
        cursor = await conn.execute(smtp)
        rows = await cursor.fetchall()
        song_insert = [dict(r) for r in rows]

    text = get_song_text(song_insert)
    await TelegramSDK().send_message(chat_id=message['chat_id'], message=text)
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
    queue_name = RABBITMQ_QUERY

    # Creating channel
    channel = await app.aio_pika.channel()

    # Declaring queue
    queue = await channel.declare_queue(
        queue_name,
        durable=True,
    )

    await queue.consume(consumer_bot_message)

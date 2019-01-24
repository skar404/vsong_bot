import json
from time import time

from aio_pika import Message
from sanic.log import logger
from sqlalchemy import insert
from vk_api.audio import VkAudio
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

from app.clients.telegram import TelegramSDK
from app.bot.handler import RabbitMessageType
from app.models import MusicModel
from app.settings import RABBITMQ_EXCHANGE, RABBITMQ_QUERY, PROXY_FULL_URL


@compiles(Insert)
def append_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'append_string' in insert.kwargs:
        return s + " " + insert.kwargs['append_string']
    return s


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
    return '\n'.join([f'{i}. {song["artist"]} - {song["title"]} ({song["duration"]})\n/song\_{i}'
                      for i, song in enumerate(song_list, 1)])


async def send_song_list(message):
    from app import application

    song_list = await get_vk_song_list(message['text'])

    telegram = TelegramSDK()

    query = insert(MusicModel, append_string='ON CONFLICT DO NOTHING RETURNING *;').values(song_list)
    async with application.pg_client.acquire() as conn:
        cursor = await conn.execute(query)
        rows = await cursor.fetchall()
        song_download = [dict(r) for r in rows]

    text = get_song_text(song_list)

    await telegram.send_message(chat_id=message['chat_id'], message=text)
    await telegram.delete_message(chat_id=message['chat_id'], message_id=message['message_id'])

    channel = await application.aio_pika.channel()
    exchange = await channel.declare_exchange(RABBITMQ_EXCHANGE)

    for song in song_download:
        await exchange.publish(
            Message(json.dumps({
                'type': RabbitMessageType.DOWNLOAD_SONG,
                'song_info': {
                    'id': song['id'],
                    'url': song['v_url'],
                    'artist': song['artist'],
                    'title': song['title']
                }
            }).encode()),
            routing_key=RABBITMQ_QUERY,
        )


async def download_song(message):
    from app import application
    async with application.aiohttp_session.get(message['song_info']['url']) as response:
        while True:
            chunk = await response.content.read(16144)
            if not chunk:
                break


SWITCH = {
    RabbitMessageType.SEND_SONG_LIST: send_song_list,
    RabbitMessageType.DOWNLOAD_SONG: download_song
}


async def consumer_bot_message(message):
    logger.info('start consumer download_song')
    with message.process():
        message_body = json.loads(message.body)

        await SWITCH[message_body['type']](message_body)

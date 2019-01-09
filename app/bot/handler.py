import json

from aio_pika import Message

from app import TelegramSDK
from app.bot.router import TelegramRouter
from app.settings import BOT_TOKEN, RABBITMQ_QUERY, RABBITMQ_EXCHANGE

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


class RabbitMessageType:
    DOWNLOAD_SONG = 'DOWNLOAD_SONG'


@bot_handler.command(command='start')
async def send_message(message, _request):
    text = 'Привет @{user_name},\n' \
        'Просто отправь мне имя артиста и/или название композиции,\n' \
        'и я найду эту песню для тебя!'.format(user_name=message['message']['from']['username'])

    await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


@bot_handler.text()
async def get_track(message, request):
    chat_id = message['message']['chat']['id']
    song_text = message['message']['text']

    text = 'Начал искать трек: *{message}*'\
        .format(message=song_text)

    req = await TelegramSDK().send_message(chat_id=chat_id, message=text)

    message_id = req['result']['message_id']

    channel = await request.app.aio_pika.channel()
    exchange = await channel.declare_exchange(RABBITMQ_EXCHANGE)

    await exchange.publish(
        Message(json.dumps({
            'type': RabbitMessageType.DOWNLOAD_SONG,
            'chat_id': chat_id,
            'message_id': message_id,
            'text': song_text
        }).encode()),
        routing_key=RABBITMQ_QUERY,
    )

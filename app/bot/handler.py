from app import TelegramSDK
from app.bot.router import TelegramRouter
from app.settings import BOT_TOKEN

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


@bot_handler.command(command='start')
async def send_message(message, _request):
    text = 'Привет @{user_name},\n' \
        'Просто отправь мне имя артиста и/или название композиции,\n' \
        'и я найду эту песню для тебя!'.format(user_name=message['message']['from']['username'])

    await TelegramSDK() \
        .send_message(chat_id=message['message']['chat']['id'], message=text)


@bot_handler.text()
async def get_track(message, _request):
    text = 'Начал искать трек: *{message}*'\
        .format(message=message['message']['text'])

    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message=text)

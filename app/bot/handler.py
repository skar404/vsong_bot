from app import TelegramSDK
from app.bot.router import TelegramRouter
from app.settings import BOT_TOKEN

bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


@bot_handler.command(command='start')
async def send_message(message):
    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message="""
        Привет @{user_name},
        Просто отправь мне имя артиста и/или название композиции,
        и я найду эту песню для тебя!
        """.format(user_name=message['message']['chat']['username']))


@bot_handler.text()
async def get_track(message):
    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message="""
    Начал искать трек: *{message}*""".format(message=message['message']['text']))

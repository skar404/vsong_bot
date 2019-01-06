from sanic import Blueprint
from sanic.response import json

from app import TelegramSDK
from app.bot.router import TelegramRouter
from app.schemas.Telegram import WebHookMessageSchema
from app.settings import BOT_SECRET_URL, BOT_TOKEN
from app.shortcuts.validation import validation_shame
from app.shortcuts.view import success

bp = Blueprint('default')


@bp.get('ping')
async def ping(_request):
    return success()


@bp.get('test')
async def get_test(request):
    return json(
        await TelegramSDK().update_web_hook()
    )


bot_handler = TelegramRouter(bot_token=BOT_TOKEN)


@bot_handler.command(command='start')
async def send_message(message):
    await TelegramSDK().send_message(chat_id=message['message']['chat']['id'], message="""
        Привет @{user_name},
        Просто отправь мне имя артиста и/или название композиции,
        и я найду эту песню для тебя!
        """.format(user_name=message['message']['chat']['username']))


@bp.post('bot/{secret_url}'.format(secret_url=BOT_SECRET_URL))
@validation_shame(WebHookMessageSchema)
async def bot(request):
    await bot_handler.init_route(request['valid_data'])

    return success()

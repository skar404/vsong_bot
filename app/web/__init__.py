from sanic import Blueprint
from sanic.response import json

from app import TelegramSDK
from app.bot.handler import bot_handler
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


@bp.post('bot/{secret_url}'.format(secret_url=BOT_SECRET_URL))
@validation_shame(WebHookMessageSchema)
async def bot(request):
    await bot_handler.init_route(request['valid_data'])

    return success()

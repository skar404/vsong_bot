from sanic import Blueprint
from sanic.response import json

from app import TelegramSDK
from app.schemas.Telegram import WebHookMessageSchema
from app.settings import BOT_SECRET_URL
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

    await TelegramSDK().send_message(chat_id='', message='test')

    return success()

from sanic import Blueprint
from sanic.response import json

from app import TelegramSDK
from app.settings import BOT_SECRET_URL
from app.shortcuts.telegram import user_info
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
@user_info
async def bot(request):
    await TelegramSDK().send_message(chat_id='', message='test')

    return success()

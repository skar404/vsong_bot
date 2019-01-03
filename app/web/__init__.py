from sanic import Blueprint

from app.shortcuts.view import success

bp = Blueprint('default')
bp_bot = Blueprint('bot')


@bp.get('/ping')
async def test(_request):
    return success()

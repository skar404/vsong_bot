from marshmallow import ValidationError

from app.schemas.Telegram import WebHookMessageShame
from app.shortcuts.view import marshmallow_errors


def user_info(func):

    async def wrapper(request, *args, **kwargs):
        try:
            req = WebHookMessageShame().load(request.json)
        except ValidationError as err:
            return marshmallow_errors(err.messages)

        request['message_info'] = dict(req)

        res = await func(request, *args, **kwargs)
        return res

    return wrapper

from marshmallow import ValidationError

from app.shortcuts.view import marshmallow_errors


def validation_shame(schema):
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            try:
                req = schema().load(request.json)
            except ValidationError as err:
                return marshmallow_errors(err.messages)

            request['valid_data'] = dict(req)

            res = await func(request, *args, **kwargs)
            return res

        return wrapper

    return decorator

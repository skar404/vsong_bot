from sanic.response import json


class ReturnStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


def success():
    return json({
        'status': ReturnStatus.SUCCESS
    })


def bad_request():
    return json({
        'status': ReturnStatus.ERROR
    }, status=400)


def marshmallow_errors(errors: dict):
    return json({
        'status': ReturnStatus.ERROR,
        'errors': errors
    }, status=400)

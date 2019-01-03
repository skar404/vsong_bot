from sanic.response import json


class ReturnStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


def success():
    return json({
        'status': ReturnStatus.SUCCESS
    })

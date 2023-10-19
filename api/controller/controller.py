from typing import Tuple
from flask import request, make_response
import json
import datetime
import dataclasses

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            elif isinstance(o, datetime.datetime):
                return o.isoformat()
            return super().default(o)

@staticmethod
def handle(status: str, data: any = None, success: bool = False):
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    if request.method == 'OPTIONS':
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
    response.status = status
    response.content_type = 'application/json'
    response.data = json.dumps({"success": success, "data": data}, cls=EnhancedJSONEncoder)
    return response

@staticmethod
def OK(result = None) -> Tuple:
    return handle('200 OK', result, True)

@staticmethod
def Posted(result = None) -> Tuple:
    return handle('201 POSTED', result, True)

@staticmethod
def UnAuthorized(result = None) -> Tuple:
    return handle('401 UNAUTHORIZED', result, False)

@staticmethod
def BadRequest(result = None) -> Tuple:
    return handle('400 BAD REQUEST', result, False)

from typing import List, Optional, Tuple, Union, get_origin, get_args
from flask import request, make_response
import json
import datetime
import dataclasses
import sqlalchemy.orm as sqldb

from api.loghandler.logger import Logger

class EnhancedJSONEncoder(json.JSONEncoder):
  def default(self, o):
      if dataclasses.is_dataclass(o):
          return dataclasses.asdict(o)
      elif isinstance(o, datetime.datetime):
          return o.isoformat()
      elif isinstance(o, BaseException):
          return str(o)
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
def HandleGet(result: any) -> Tuple:
    if result is None or result == []:
        return NotFound()
    return OK(result)

@staticmethod
def OK(result = None) -> Tuple:
    return handle('200 OK', result, True)

@staticmethod
def NotFound(result = None) -> Tuple:
    return handle('404 NOT FOUND', result, False)

@staticmethod
def Forbidden(result = None) -> Tuple:
    return handle('403 FORBIDDEN', result, False)

@staticmethod
def Posted(result = None) -> Tuple:
    return handle('201 POSTED', result, True)

@staticmethod
def UnAuthorized(result = None) -> Tuple:
    return handle('401 UNAUTHORIZED', result, False)

@staticmethod
def BadRequest(result = None) -> Tuple:
    return handle('400 BAD REQUEST', result, False)

@staticmethod
def Conflict(result = None) -> Tuple:
    return handle('409 CONFLICT', result, False)

@staticmethod
def ServerError(result = None) -> Tuple:
    Logger.error(f"A server error was explicitly thrown, {result}")
    return handle('500 SERVER ERROR', result, False)

@staticmethod
def validRequestDataFor(json: dict, model: any) -> bool:
    try:
        model(**json)

        testFlag = True
        errors = []

        for field in dataclasses.fields(model):
            if field.name == 'id': continue # Skip the default auto-incrementing id field
            if _is_optional(field.type): continue
            if _is_mapped_type(field.type): continue
            if _is_mapped_list_type(field.type): continue
            if field.name not in json.keys():
                Logger.error(f"Invalid request data for model {model.__name__}, missing field {field.name}")
                errors.append(f"Missing required field {field.name}")
                testFlag = False
        return testFlag, errors
    except TypeError as typeError:
        Logger.error(f"Invalid request data for model {model.__name__}", typeError)
        return False, [typeError]
    except Exception as exception:
        Logger.error(f"Unknown error in request for model {model.__name__}", exception)
        return False, [exception]

@staticmethod
def _is_optional(obj_type):
    if get_origin(obj_type) is Union and type(None) in get_args(obj_type):
        return True
    return False

@staticmethod
def _is_mapped_list_type(obj_type):
    if getattr(obj_type, '__origin__', None) is sqldb.Mapped:
        inner_type = getattr(obj_type, '__args__', [])[0]
        print(inner_type)
        if inner_type.__origin__ == list:
            return True
    return False

@staticmethod
def _is_mapped_type(obj_type):
    if getattr(obj_type, '__origin__', None) is sqldb.Mapped:
        return True
    return False

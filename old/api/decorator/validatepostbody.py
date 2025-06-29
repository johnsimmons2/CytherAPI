from flask import request
from api.controller.controller import BadRequest


def validate_post_body(validatorFn, serviceMember):
  def decorator(func):
    def wrapper(*arg, **kwargs):
      if request.get_json() is None:
        return BadRequest('No JSON was provided for the spell.')

      _data = request.get_json()

      _nestedData = { k:v for (k,v) in _data.items() if isinstance(v, dict) }
      _json = { k:v for (k,v) in _data.items() if not isinstance(v, dict) }

      # We pass only the top level json data to be validated.
      _isValid, _errors = validatorFn(_json, serviceMember)
      if _isValid:
        _instance = serviceMember(**_json)
        kwargs.update({'nestedData': _nestedData})
        return func(_instance, *arg, **kwargs)
      else:
        return BadRequest(_errors)
    wrapper.__name__ = func.__name__
    return wrapper
  return decorator

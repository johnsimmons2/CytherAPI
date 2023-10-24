from api.service.jwthelper import get_access_token, verify_token, decode_token
from api.controller import UnAuthorized, BadRequest
from jwt import InvalidSignatureError
from api.service.dbservice import UserService
import os


def isAdmin(func):
  def wrapper(*arg, **kwargs):
    try:
      if os.getenv('ENVIRONMENT') == 'development':
        return func(*arg, **kwargs)
      token = decode_token(get_access_token())
      if token is None:
        return BadRequest('The token is not valid.')
      user = UserService.getByUsername(token['username'])
      for role in user.roles:
        if role.level == 0:
            return func(*arg, **kwargs)
      return UnAuthorized('The user does not have authorization for this route.')
    except InvalidSignatureError:
      return UnAuthorized('The token is not valid.')
  wrapper.__name__ = func.__name__
  return wrapper

def isPlayer(func):
  def wrapper(*arg, **kwargs):
    try:
      if os.getenv('ENVIRONMENT') == 'development':
        return func(*arg, **kwargs)
      token = decode_token(get_access_token())
      if token is None:
        return BadRequest('The token is not valid.')
      user = UserService.getByUsername(token['username'])
      for role in user.roles:
        if role.level <= 1:
            return func(*arg, **kwargs)
      return UnAuthorized('The user does not have authorization for this route.')
    except InvalidSignatureError:
      return UnAuthorized('The token is not valid.')
  wrapper.__name__ = func.__name__
  return wrapper

def isAuthorized(func):
  def wrapper(*arg, **kwargs):
    if os.getenv('ENVIRONMENT') == 'development':
      return func(*arg, **kwargs)
    tok = get_access_token()
    verified = verify_token(tok)
    if verified:
      return func(*arg, **kwargs)
    else:
      return UnAuthorized('The access token is invalid or expired.')
  wrapper.__name__ = func.__name__
  return wrapper

def userOwnsId(func):
  def wrapped(*arg, **kwargs):
    if os.getenv('ENVIRONMENT') == 'development':
      return func(*arg, **kwargs)
    token = decode_token(get_access_token())
    if token is None:
      return BadRequest('The token is not valid.')
    user = UserService.getByUsername(token['username'])
    if 'id' in kwargs:
      if user.id == kwargs['id']:
        return func(*arg, **kwargs)
      else:
        return UnAuthorized('The current user does not have permission for this action')
  wrapped.__name__ = func.__name__
  return wrapped

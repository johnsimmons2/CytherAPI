import json
import datetime
import os
import jwt
from api.service.config import config
from api.loghandler.logger import Logger
from api.model.user import User
from flask import request


def get_username() -> str:
    token = decode_token(get_access_token())
    if token is None: return None
    return token['username']

def has_role_level(level: int) -> bool:
    token = decode_token(get_access_token())
    if token is None: return False
    for role in token['roles']:
        if role['level'] <= level:
            return True
    return False

def create_token(user: User) -> str:
    return jwt.encode({
        'username': user.username,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'roles': [{'roleName': role.roleName, 'level': role.level} for role in user.roles]
        }, os.getenv('JWT_SECRET'), "HS256")

def decode_token(token: str) -> dict:
    try:
        jwtsecret = os.getenv('JWT_SECRET')
        result = jwt.decode(token, jwtsecret, "HS256")
        return result
    except Exception as exception:
        Logger.error('JWT Token decoding failed due to exception.', exception)
    return None

def verify_token(token: str) -> bool:
    try:
        jwtsecret = os.getenv('JWT_SECRET')
        result = jwt.decode(token, jwtsecret, "HS256")
        expired = datetime.datetime.utcnow() > datetime.datetime.utcfromtimestamp(result['exp'])
        print(result)
        if expired:
            Logger.warn('JWT Token is expired')
            return False
    except Exception as exception:
        Logger.error(f'JWT Token validation failed due to exception. Token: {token}', exception)
        return False
    return True

def get_access_token():
    if request.headers and 'Authorization' in request.headers.keys():
        data = request.headers['Authorization']
    elif request.form and 'Authorization' in request.form.keys():
        data = request.form['Authorization']
    elif request.data and request.data['Authorization']:
        data = json.loads(data)
        data = request.data['Authorization']
    elif request.args and 'token' in request.args.keys():
        data = request.args['token']
    else:
        Logger.error('Authorization was not supplied.')
        return None
    try:
        # Check if data is already a token
        if 'Bearer' in data:
            return data.split(' ')[1]
        return data
    except Exception:
        Logger.error('Token was not supplied in "Bearer TOKEN" format.')
    return None

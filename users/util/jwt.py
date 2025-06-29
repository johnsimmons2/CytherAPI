import hashlib
import logging
import json
import datetime
import os
import jwt
import logging
from decouple import config
from users.models import User
from django.utils import timezone


logger = logging.getLogger(__name__)

def hash_password(cls, password: str, salt: str) -> str:
    secret = config('security')
    try:
        sha = hashlib.sha256()
        sha.update(password.encode(encoding = 'UTF-8', errors = 'strict'))
        sha.update(':'.encode(encoding = 'UTF-8'))
        sha.update(salt.encode(encoding = 'UTF-8', errors = 'strict'))
        sha.update(secret['usersecret'].encode(encoding = 'UTF-8', errors = 'strict'))
        return sha.hexdigest()
    except Exception as error:
        logger.error(error)
    return None

def create_token(user: User) -> str:
    return jwt.encode({
            'username': user.username,
            'userId': user.id,
            'email': user.email,
            'exp': timezone.now() + datetime.timedelta(minutes=120),
            'roles': [
                role for role in user.roles
                ]
        }, config('JWT_SECRET'), "HS256")
import hashlib
from api.model.user import User
from api.service.config import config
from api.loghandler.logger import Logger

# TODO: This needs to be moved to the auth-api project. The Auth methods in this project will
# only callout to the auth-api project and await results. This project will not ever
# return or keep plaintext passwords 

class AuthRepo:
    @classmethod
    def isAuthorized(cls, user: User, secret: str) -> User | None:
        # Request the auth-api project to see if a given user and secret combo
        pass
    
    @classmethod
    def _hash_password(cls, password: str, salt: str) -> str:
        secret = config('security')
        try:
            sha = hashlib.sha256()
            sha.update(password.encode(encoding = 'UTF-8', errors = 'strict'))
            sha.update(':'.encode(encoding = 'UTF-8'))
            sha.update(salt.encode(encoding = 'UTF-8', errors = 'strict'))
            sha.update(secret['usersecret'].encode(encoding = 'UTF-8', errors = 'strict'))
            return sha.hexdigest()
        except Exception as error:
            Logger.error(error)
        return None

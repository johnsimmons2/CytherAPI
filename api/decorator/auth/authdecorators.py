from api.service.jwthelper import get_access_token, verify_token, decode_token
from api.controller import UnAuthorized, BadRequest, Forbidden
from jwt import InvalidSignatureError
from api.service.dbservice import UserService
import os


def isAdmin(func):
	def wrapper(*arg, **kwargs):
		try:
			token = decode_token(get_access_token())
			if token is None:
				return UnAuthorized("The token is not valid.")
			user = UserService.getByUsername(token["username"])

			if user is None:
				return UnAuthorized("The user does not exist.")

			for role in user.roles:
				if role.level == 0:
					return func(*arg, **kwargs)
			return Forbidden("The user does not have authorization for this route.")
		except InvalidSignatureError:
			return UnAuthorized("The token is not valid.")

	wrapper.__name__ = func.__name__
	return wrapper


def isPlayer(func):
    def wrapper(*arg, **kwargs):
        try:
            token = decode_token(get_access_token())
            if token is None:
                return UnAuthorized("The token is not valid.")
            user = UserService.getByUsername(token["username"])

            if user is None:
                return UnAuthorized("The user does not exist.")

            for role in user.roles:
                if role.level <= 1:
                    return func(*arg, **kwargs)
            return Forbidden("The user does not have authorization for this route.")
        except InvalidSignatureError:
            return UnAuthorized("The token is not valid.")

    wrapper.__name__ = func.__name__
    return wrapper


def isAuthorized(func):
    def wrapper(*arg, **kwargs):
        tok = get_access_token()
        verified = verify_token(tok)
        if verified:
            return func(*arg, **kwargs)
        else:
            return UnAuthorized("The access token is invalid or expired.")

    wrapper.__name__ = func.__name__
    return wrapper


def userOwnsId(func):
    def wrapped(*arg, **kwargs):
        token = decode_token(get_access_token())
        if token is None:
            return BadRequest("The token is not valid.")
        user = UserService.getByUsername(token["username"])

        if user is None:
            return BadRequest("The user does not exist.")

        if "id" in kwargs:
            if user.id == kwargs["id"]:
                return func(*arg, **kwargs)
            else:
                return Forbidden(
                    "The current user does not have permission for this action"
                )

    wrapped.__name__ = func.__name__
    return wrapped

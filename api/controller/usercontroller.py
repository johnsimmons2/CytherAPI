import json
from flask import Blueprint, request
from api.service.dbservice import UserService
from api.model.user import User
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.controller import OK, UnAuthorized, BadRequest, Posted
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService


users = Blueprint('users', __name__)

@users.route("/users", methods = ['GET'])
@isAdmin
@isAuthorized
def get():
    return UserService.getAll()

@users.route("/users/<id>", methods = ['GET'])
@isAuthorized
def getUser(id: str):
    return UserService.get(id)

@users.route("/users/<id>", methods = ['POST'])
@isAuthorized
def updateUser(id: str):
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    user = User(**json.loads(request.data))
    UserService.updateUser(id, user)
    return OK()

@users.route("/auth", methods = ['GET'])
@isAuthorized
def checkAuth():
    return OK()

@users.route("/auth/token", methods = ['POST'])
def authenticate():
    if request.get_json() is None:
        return BadRequest('User was not provided or something was wrong with the input fields.')
    
    user = User(**json.loads(request.data))
    if user.password is None:
        return BadRequest('No password was provided.')

    if user.username is None and user.email is None:
        return BadRequest('No username or email was provided.')
    
    authenticated = AuthService.authenticate_user(user)
    if authenticated is not None:
        return OK(dict({"token": str(authenticated)}))
    else:
        return UnAuthorized("Whoza whutsit?!")

@users.route("/auth/register", methods = ['POST'])
def post():
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    
    user = User(**json.loads(request.data))
    if user.password is None:
        return BadRequest('No password was provided.')

    if user.username is None and user.email is None:
        return BadRequest('No username or email was provided.')
    
    if UserService.exists(user):
        return BadRequest('User already exists with that email or username.')

    return Posted(AuthService.register_user(user))

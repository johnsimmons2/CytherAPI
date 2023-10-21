import json
from flask import Blueprint, request, jsonify
from api.service.dbservice import UserService, RoleService
from api.model.user import User, Role
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.controller import OK, UnAuthorized, BadRequest, Posted
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService


users = Blueprint('users', __name__)

@users.route("/users", methods = ['GET'])
@isAdmin
@isAuthorized
def get():
    return OK(UserService.getAll())

@users.route("/users/<id>", methods = ['GET'])
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

@users.route("/users/<id>/roles", methods = ['GET'])
@isAuthorized
@isAdmin
def getUserRoles(id: str):
    result = UserService.get(id).roles
    if result is None:
        return BadRequest('No user was found with that ID.')
    return OK(result)

@users.route("/users/<id>/roles", methods = ['POST'])
@isAuthorized
@isAdmin
def updateUserRoles(id: str):
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    roles = [role for role in json.loads(request.data)]
    userRoles: list[Role] = []
    if not isinstance(roles, list):
        return BadRequest('Roles must be a list of roles.')
    for role in roles:
        if role['level'] is None:
            return BadRequest('Roles must have a level.')
        userRoles.append(RoleService.roleWithLevel(role['level']))

    UserService.updateUserRoles(id, userRoles)
    return OK()

@users.route("/auth", methods = ['GET'])
@isAuthorized
def checkAuth():
    return OK(UserService.getCurrentUserRoles())

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

@users.route("/roles", methods = ['GET'])
def getRoles():
    return OK(RoleService.getAll())

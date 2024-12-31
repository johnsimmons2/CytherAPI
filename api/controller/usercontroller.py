import json
from flask import Blueprint, request, jsonify
from api.service.dbservice import UserService, RoleService
from api.model.user import User, Role
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.controller import OK, UnAuthorized, BadRequest, Posted, Conflict, NotFound
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService
from api.loghandler.logger import Logger
import api.service.jwthelper as jwth


users = Blueprint('users', __name__)

@users.route("/users", methods = ['GET'])
@isAdmin
def get():
    return OK(UserService.getAll())

@users.route("/users/<id>", methods = ['GET'])
@isAuthorized
def getUser(id: str):
    if id is None or id == '':
        return BadRequest('No user ID was provided.')
    if id.isdigit():
        user = UserService.get(id)
        if user:
            return OK(user)
        else:
            return NotFound('No user was found with that ID.')
    else:
        user = UserService.getByUsername(id)
        if user:
            return OK(user)
        else:
            return NotFound('No user was found with that username.')

@users.route("/users/<id>", methods = ['DELETE'])
@isAdmin
def deleteUser(id: str):
    if id is None or id == '' or id == '1':
        return BadRequest("Cannot delete user with given ID of {id}".format(id=id))
    deleted = UserService.delete(id)
    if deleted:
        return OK()
    else:
        return BadRequest('No user was found with that ID.')

@users.route("/users/<id>", methods = ['PATCH'])
@isAuthorized
def updateUser(id: str):
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    user = User.from_dict(json.loads(request.data))
    Logger.debug(f"Updating user: {user.id} - {user.username}")
    UserService.updateUser(id, user)
    return OK()

@users.route("/users/<id>/roles", methods = ['GET'])
@isAdmin
def getUserRoles(id: str):
    result = UserService.get(id)
    if result is None:
        return BadRequest('No user was found with that ID.')
    return OK(result.roles)

@users.route("/users/<id>/roles", methods = ['PATCH'])
@isAdmin
def updateUserRoles(id: str):
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')

    rolesJson = json.loads(request.data)
    if not 'roles' in rolesJson:
        return BadRequest('No roles were provided.')
    roles = rolesJson['roles']
    userRoles: list[Role] = []
    for role in roles:
        if isinstance(role, int):
            userRoles.append(RoleService.get(role))
            continue
        elif not isinstance(role, dict):
            return BadRequest('Roles must be a list of roles.')
        if role['level'] is None:
            return BadRequest('Roles must have a level.')
        userRoles.append(RoleService.roleWithLevel(role['level']))

    Logger.debug(userRoles)
    UserService.updateUserRoles(id, userRoles)
    return OK()

@users.route("/roles", methods = ['GET'])
def getRoles():
    return OK(RoleService.getAll())


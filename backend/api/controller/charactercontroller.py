import json
from flask import Blueprint, request
from api.service.dbservice import CharacterService
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.controller import OK, UnAuthorized, BadRequest, Posted
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService


characters = Blueprint('characters', __name__)

@characters.route("/characters", methods = ['GET'])
@isAdmin
@isAuthorized
def get():
    return OK(CharacterService.getAll())

@characters.route("/characters/player", methods = ['GET'])
@isAuthorized
def getPlayerCharacters():
    return OK(CharacterService.getPlayerCharacters())
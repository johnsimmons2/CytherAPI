import json
from flask import Blueprint, request
from api.model.character import Character
from api.service.dbservice import CharacterService
from api.decorator.auth.authdecorators import isAuthorized, isAdmin, isPlayer
from api.controller import OK, UnAuthorized, BadRequest, Posted, HandleGet
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService


characters = Blueprint('characters', __name__)

@characters.route("/characters", methods = ['GET'])
@isAdmin
@isAuthorized
def get():
    userId = request.args.get('userId', default=None)
    if userId is not None:
        # If the user passes the query parameter ?userId then we will return all characters for that user.
        return HandleGet(CharacterService.getCharactersByUserId(userId))
    return HandleGet(CharacterService.getAll())

@characters.route("/characters/player", methods = ['GET'])
@isAuthorized
def getAllPlayerCharacters():
    return HandleGet(CharacterService.getAllPlayerCharacters())

@characters.route("/characters/player", methods = ['GET'])
@isAdmin
@isAuthorized
def getAllNPCs():
    return HandleGet(CharacterService.getAllNPCs())

@characters.route("/characters/<id>", methods = ['GET'])
@isAuthorized
def getCharacter(id: str):
    return HandleGet(CharacterService.get(id))

@characters.route("/characters", methods = ['POST'])
@isPlayer
@isAuthorized
def makeCharacter():
    if request.get_json() is None:
        return BadRequest('No character was provided or the input was invalid.')

    characterJson = json.loads(request.data)
    createdId, errors = CharacterService.createCharacter(characterJson)
    print(createdId, errors)
    if createdId:
        return Posted({"characterId": createdId})
    return BadRequest(errors)

@characters.route("/characters/<id>", methods = ['PATCH'])
@isAdmin
@isAuthorized
def updateCharacter(id: str):
    if request.get_json() is None:
        return BadRequest('No character was provided or the input was invalid.')
    characterJson = json.loads(request.data)
    success, errors = CharacterService.updateCharacter(id, characterJson)
    if success:
        return Posted()
    else:
        return BadRequest(errors)

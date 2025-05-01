import json
from flask import Blueprint, request, jsonify
from api.controller.controller import NotFound
from api.loghandler.logger import Logger
from api.model.character import Character
from api.model.user import UserCharacters
from api.model.dto.characterDto import CharacterDTO, CharacterDescriptionDTO
from api.model.dto.spellbookDto import SpellbookDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.service.repo.characterservice import CharacterService
from api.decorator.auth.authdecorators import isAuthorized, isAdmin, isPlayer
from api.controller import OK, UnAuthorized, BadRequest, Posted, HandleGet
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService, UserService
from api.service.rolehelper import get_userdto_from_token


characters = Blueprint("characters", __name__)


@characters.route("/characters", methods=["GET"])
@isPlayer
def get():
    userId = request.args.get("username", default=None)
    result = []
    if userId is not None:
        # If the user passes the query parameter ?userId then we will return all characters for that user.
        userId = UserService.getByUsername(userId).id
        charactersForUser = CharacterService.getCharactersByUserId(userId)
        result = [ {"character": char, "userId": userId} for char in charactersForUser ]
        return OK(result)
    
    allCharacters = CharacterService.getAll()
    result = [ { "character": char, "userId": CharacterService.getOwnerIdFor(char.id) } for char in allCharacters ]
    return OK(result)

@characters.route("/characters/player", methods=["GET"])
@isAuthorized
def getAllPlayerCharacters():
    return HandleGet(CharacterService.getAllPlayerCharacters())

@characters.route("/characters/npc", methods=["GET"])
@isAdmin
def getAllNPCs():
    return HandleGet(CharacterService.getAllNPCs())

@characters.route("/characters/<id>", methods=["GET"])
@isAuthorized
def getCharacter(id: str):
    if id is None or id == '':
        return BadRequest('No character ID was provided.')
    if id.isdigit():
        character = CharacterService.get(id)
        if character:
            return OK(character)
        else:
            return NotFound('No character was found with that ID.')
    else:
        character = CharacterService.getCharacterByName(id)
        if character:
            return OK(character)
        else:
            return NotFound('No character was found with that username.')

@characters.route("/characters", methods=["POST"])
@isPlayer
def makeCharacter():
    if request.get_json() is None:
        return BadRequest("No character was provided or the input was invalid.")

    characterDTO: CharacterDTO
    userDTO = get_userdto_from_token()

    try:
        characterJson = json.loads(request.data)
        statsheetDto = StatsheetDTO(**characterJson["stats"])
        spellbookDto = SpellbookDTO(**characterJson["spellbook"])
        characterJson["stats"] = statsheetDto
        characterJson["spellbook"] = spellbookDto
        if "description" in characterJson:
            characterJson["description"] = CharacterDescriptionDTO(
                **characterJson["description"]
            )

        characterDTO = CharacterDTO(**characterJson)
    except Exception as e:
        return BadRequest(e)

    try:
        createdId = CharacterService.createCharacter(characterDTO, userDTO)

        if createdId:
            return Posted({"characterId": createdId})
    except Exception as e:
        return BadRequest(e)

@characters.route("/characters/<id>", methods=["PATCH"])
@isAdmin
def updateCharacter(id: str):
    if request.get_json() is None:
        return BadRequest("No character was provided or the input was invalid.")
    characterJson = json.loads(request.data)
    success, errors = CharacterService.updateCharacter(id, characterJson)
    if success:
        return Posted()
    else:
        return BadRequest(errors)

@characters.route("/characters/users/<id>", methods=["PATCH"])
@isAdmin
def updateCharacterOwner(id: str):
    if request.get_json() is None:
        return BadRequest("No userId was provided or the input was invalid.")
    req = json.loads(request.data)
    try:
        result = CharacterService.updateUserCharacters(id, req["characterId"])
        return OK(result)
    except Exception as e:
        Logger.error(e)
        return BadRequest(e)

@characters.route("/characters/users", methods=["GET"])
@isAdmin
def getAllCharactersByUser():
    characters: list[Character] = CharacterService.getAll()
    userCharacters: list[UserCharacters] = CharacterService.getUserCharacters()
    result = {}
    for character in characters:
        print(character.id)
        foundUser = False
        result.update({character.id: {}})
        for userCharacter in userCharacters:
            if character.id == userCharacter.characterId:
                Logger.debug(f"Found user character: {userCharacter.id} - {userCharacter.characterId}")
                result[character.id].update({"character": character})
                result[character.id].update({"userId": userCharacter.userId})
                foundUser = True
                continue
        else:
            if not foundUser:
                result[character.id].update({"character": character})
                result[character.id].update({"userId": None})
    return OK(result)
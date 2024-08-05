import json
from flask import Blueprint, request
from api.model.character import Character
from api.model.dto.characterDto import CharacterDTO, CharacterDescriptionDTO
from api.model.dto.spellbookDto import SpellbookDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.service.repo.characterservice import CharacterService
from api.decorator.auth.authdecorators import isAuthorized, isAdmin, isPlayer
from api.controller import OK, UnAuthorized, BadRequest, Posted, HandleGet
from api.service.jwthelper import create_token
from api.service.dbservice import AuthService
from api.service.rolehelper import get_userdto_from_token


characters = Blueprint("characters", __name__)


@characters.route("/characters", methods=["GET"])
@isAdmin
@isAuthorized
def get():
    userId = request.args.get("userId", default=None)
    if userId is not None:
        # If the user passes the query parameter ?userId then we will return all characters for that user.
        return HandleGet(CharacterService.getCharactersByUserId(userId))
    return HandleGet(CharacterService.getAll())


@characters.route("/characters/player", methods=["GET"])
@isAuthorized
def getAllPlayerCharacters():
    return HandleGet(CharacterService.getAllPlayerCharacters())


@characters.route("/characters/npc", methods=["GET"])
@isAuthorized
@isAdmin
def getAllNPCs():
    return HandleGet(CharacterService.getAllNPCs())


@characters.route("/characters/<id>", methods=["GET"])
@isAuthorized
def getCharacter(id: str):
    return HandleGet(CharacterService.get(id))


@characters.route("/characters", methods=["POST"])
@isPlayer
@isAuthorized
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
@isAuthorized
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

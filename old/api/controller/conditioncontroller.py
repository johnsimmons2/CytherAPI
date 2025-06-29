import json
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.campaign import Campaign
from api.model.user import User
from api.service.dbservice import UserService
from api.service.repo.characterservice import CharacterService
from api.service.repo.campaignservice import CampaignService
from api.service.repo.conditionsservice import ConditionsService


conditions = Blueprint('conditions', __name__)

@conditions.route("/conditions", methods = ['GET'])
@isAuthorized
def get():
    return OK(ConditionsService.getAll())

@conditions.route("/conditions/<id>", methods = ['GET'])
@isAuthorized
def getById():
    condition = ConditionsService.get(id)
    if condition is None:
        return NotFound('No condition was found with that ID.')
    return OK(condition)

@conditions.route("/conditions/<condId>/characters/<charId>", methods = ['POST'])
@isAdmin
def addConditionToCharacter(condId: str, charId: str):
    condition = ConditionsService.get(condId)
    character = CharacterService.get(charId)
    if condition is None or character is None:
        return NotFound('No condition or character was found with that ID.')
    
    deleteTag = request.args.get('delete')
    if deleteTag is None:
        success = ConditionsService.addConditionToCharacter(condId, charId)
    else:
        success = ConditionsService.removeConditionFromCharacter(condId, charId)
    if success:
        return Posted('Condition added to character.')
    return BadRequest("The condition could not be added to the character.")
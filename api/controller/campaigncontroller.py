import json
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.campaign import Campaign
from api.service.repo.characterservice import CharacterService
from api.service.dbservice import CampaignService


campaigns = Blueprint('campaigns', __name__)

@campaigns.route("/campaigns", methods = ['GET'])
@isAuthorized
def get():
    activeTag = request.args.get('active')
    if activeTag is None:
        return OK(CampaignService.getAll())
    else:
        if not isinstance(activeTag, bool):
            return BadRequest('The active tag must be a boolean value.')

        return OK(CampaignService.getActive(activeTag))

@campaigns.route("/campaigns/<id>", methods = ['GET'])
@isAuthorized
def getCampaign(id: str):
    result = CampaignService.get(id)
    if result is None:
        return BadRequest('No campaign was found with that ID.')
    return OK(result)

@campaigns.route("/campaigns", methods = ['POST'])
@isAuthorized
@isAdmin
def createCampaign():
    if request.get_json() is None:
        return BadRequest('No campaign was provided or the input was invalid.')

    try:
        campaign = CampaignService.create(Campaign(**json.loads(request.data)))
        return Posted(campaign)
    except Exception as e:
        return BadRequest(e)

@campaigns.route("/campaigns/<id>/characters", methods = ['GET'])
@isAuthorized
def getCampaignCharacters(id: str):
    result = CampaignService.getCharactersByCampaignID(id)
    if result is None:
        return BadRequest('No campaign was found with that ID.')
    return OK(result)

@campaigns.route("/campaigns/<id>/", methods = ['DELETE'])
@isAuthorized
@isAdmin
def deleteCampaign(id: str):
    if id is None or id == '':
        return BadRequest("Cannot delete campaign with given ID of {id}".format(id=id))
    deleted = CampaignService.delete(id)
    if deleted:
        return OK()
    else:
        return BadRequest('No campaign was found with that ID.')

@campaigns.route("/campaigns/<id>/", methods = ['POST'])
@isAuthorized
@isAdmin
def updateCampaign(id: str):
    if request.get_json() is None:
        return BadRequest('No campaign was provided or the input was invalid.')
    campaign = Campaign(**json.loads(request.data))
    CampaignService.updateCampaign(id, campaign)
    return OK()

@campaigns.route("/campaigns/<id>/characters", methods = ['POST'])
@isAuthorized
@isAdmin
def updateCampaignCharacters(id: str):
    if request.data is None:
        return BadRequest('No character IDs were provided or the input was invalid. Please provide the IDs as a list e.x: [1, 2, 3]')

    character = list(filter(lambda x: x is not None, [CharacterService.get(characterId) for characterId in json.loads(request.data)]))

    if not isinstance(character, list):
        return BadRequest('The character IDs must be a list of integers.')

    if len(character) == 0:
        return BadRequest('No characters were found with the given IDs.')

    success = CampaignService.updateCampaignCharacters(id, character)
    if success:
        return OK()
    else:
        return BadRequest('No campaign was found with that ID.')

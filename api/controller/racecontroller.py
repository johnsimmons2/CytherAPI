
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.race import Race
from api.model.feat import Feat
from api.service.repo.featservice import FeatService
from api.service.repo.raceservice import RaceService


race = Blueprint('race', __name__)

@race.route("/race", methods = ['GET'])
@isAuthorized
def get():
    races = RaceService.getAll()
    if races is not None:
        if len(races) > 0:
            return OK(races)
        else:
            return NotFound("No races could be found in the database.")
    else:
        return ServerError("The request to get races returned None instead of an empty list.")

@race.route("/race", methods = ['POST'])
@isAuthorized
@isAdmin
def createRace():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the race.')

    raceJson = request.get_json()
    feats = []

    if 'featIds' in raceJson:
        feats = _get_feats_from_json(raceJson)

        if type(feats) is str:
            return BadRequest(feats)
        del raceJson['featIds']

    if validRequestDataFor(raceJson, Race):
        newRace = Race(**raceJson)
        newRace.feats = feats
        createdId, errors = RaceService.createRace(newRace)
        if createdId > 0:
            return Posted({"raceId": createdId})
        else:
            return BadRequest(errors)
    return BadRequest("This was bad data")

@race.route("/race/<id>", methods = ['GET'])
@isAuthorized
def getRace(id: str):
    race = RaceService.get(id)
    if race is not None:
        return OK(race)
    else:
        return NotFound("Could not find race with ID")

@race.route("/race/<id>", methods = ['PATCH'])
@isAuthorized
@isAdmin
def updateRace(id: str):
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the race.')

    raceJson = request.get_json()
    feats = []

    if 'featIds' in raceJson:
        feats = _get_feats_from_json(raceJson)

        if type(feats) is str:
            return BadRequest(feats)
        del raceJson['featIds']

    if validRequestDataFor(raceJson, Race):
        raceWithId = Race(**raceJson)
        raceWithId.id = id
        createdId, errors = RaceService.update(raceWithId, feats)
        if createdId > 0:
            return Posted()
        else:
            return BadRequest(errors)
    return BadRequest("This was bad data")

@race.route("/race/<id>", methods = ['DELETE'])
@isAuthorized
@isAdmin
def deleteRace(id: str):
    success = RaceService.delete(int(id))

    if success:
        return OK()
    else:
        return NotFound("Could not find a race to delete by that ID")

def _get_feats_from_json(json):
    feats = []

    for feat in json['featIds']:
        if type(feat) is not int:
            return 'Feat must be supplied as an ID for existing feat.'
        foundFeat = FeatService.get(str(feat))
        if not foundFeat:
            return 'Was not able to get Feat with ID: ' + str(feat)
        feats.append(foundFeat)

    return feats

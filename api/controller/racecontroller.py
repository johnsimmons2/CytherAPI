
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.classes import Feat, Race
from api.service.dbservice import FeatService, RaceService


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
    if validRequestDataFor(raceJson, Race):
        createdId, errors = RaceService.createRace(Race(**raceJson))
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
    featsRefs = []

    if 'feats' in raceJson:
        for feat in raceJson['feats']:
            foundFeat = FeatService.get(feat['id'])
            if not foundFeat:
                foundFeat = FeatService.createFeat(Feat(**feat))
            featsRefs.append(foundFeat)

    del raceJson['feats']

    if validRequestDataFor(raceJson, Race):
        from api.service.dbservice import db
        raceWithId = Race(**raceJson)
        raceWithId.id = id
        createdId, errors = RaceService.update(raceWithId, feats=featsRefs)
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

from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.race import Race
from api.model.feat import Feat
from api.service.repo.featservice import FeatService


feats = Blueprint('feats', __name__)

@feats.route("/feats", methods = ['GET'])
@isAuthorized
def get():
    feats = FeatService.getAll()
    if feats is not None:
        if len(feats) > 0:
            return OK(feats)
        else:
            return NotFound("No feats could be found in the database.")
    else:
        return ServerError("The request to get feats returned None instead of an empty list.")
    
@feats.route("/feats", methods = ['POST'])
@isAdmin
def createFeat():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the feat.')
    
    featJson = request.get_json()
    if validRequestDataFor(featJson, Feat):
        created, errors = FeatService.createFeat(Feat(**featJson))
        if created:
            return Posted(created)
        else:
            return BadRequest(errors)
        
@feats.route("/feats/<id>", methods = ['PATCH'])
@isAdmin
def patchFeat(id: str):
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the feat.')
    
    featJson = request.get_json()
    if validRequestDataFor(featJson, Feat):
        feat = Feat(**featJson)
        feat.id = id
        updated, errors = FeatService.update(id, feat)
        if updated:
            return OK(updated)
        else:
            return BadRequest(errors)
    else:
        return BadRequest('The JSON provided was not valid for the feat.')

@feats.route("/feats/race", methods = ['GET'])
@isAuthorized
def getRacialFeats():
    feats = FeatService.getRacialFeats()
    if feats is not None:
        if len(feats) > 0:
            return OK(feats)
        else:
            return NotFound("No feats could be found in the database.")
    else:
        return ServerError("The request to get feats returned None instead of an empty list.")
    
@feats.route("/feats/race/<id>", methods = ['GET'])
@isAuthorized
def getRacialFeatsForRace(id: str):
    feats = FeatService.getRacialFeatsFor(id)
    if feats is not None:
        if len(feats) > 0:
            return OK(feats)
        else:
            return NotFound("Race has no feats.")
    else:
        return ServerError("The request to get feats returned None instead of an empty list.")

@feats.route("/feats/class", methods = ['GET'])
@isAuthorized
def getClassFeats():
    feats = FeatService.getClassFeats()
    if feats is not None:
        if len(feats) > 0:
            return OK(feats)
        else:
            return NotFound("No feats could be found in the database.")
    else:
        return ServerError("The request to get feats returned None instead of an empty list.")
    
@feats.route("/feats/class/<id>", methods = ['GET'])
@isAuthorized
def getClasslFeatsForClass(id: str):
    feats = FeatService.getClassFeats(id)
    if feats is not None:
        if len(feats) > 0:
            return OK(feats)
        else:
            return NotFound("Race has no feats.")
    else:
        return ServerError("The request to get feats returned None instead of an empty list.")

# ADD

@feats.route("/feats/<featId>/race/<raceId>", methods = ['POST'])
@isAdmin
def addRacialFeatToRace(featId: str, raceId: str):
    added = FeatService.addFeatToRace(featId, raceId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to race.")

@feats.route("/feats/<featId>/class/<classId>", methods = ['POST'])
@isAdmin
def addClasslFeatForClass(featId: str, classId: str):
    added = FeatService.addFeatToClass(featId, classId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to class.")
    
@feats.route("/feats/<featId>/character/<characterId>", methods = ['POST'])
@isAdmin
def addFeatForCharacter(featId: str, characterId: str):
    added = FeatService.addFeatToCharacter(featId, characterId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to class.")
    
# REMOVE
@feats.route("/feats/<featId>/race/<raceId>", methods = ['DELETE'])
@isAdmin
def addRacialFeatToRace(featId: str, raceId: str):
    added = FeatService.removeFeatFromRace(featId, raceId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to race.")

@feats.route("/feats/<featId>/class/<classId>", methods = ['DELETE'])
@isAdmin
def addClasslFeatForClass(featId: str, classId: str):
    added = FeatService.removeFeatFromClass(featId, classId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to class.")
    
@feats.route("/feats/<featId>/character/<characterId>", methods = ['DELETE'])
@isAdmin
def addFeatForCharacter(featId: str, characterId: str):
    added = FeatService.removeFeatFromCharacter(featId, characterId)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add feat to class.")

@feats.route("/feats/<id>/effects", methods = ['POST'])
@isAdmin
def addFeatEffect(id: str):
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the feat effect.')
    requestJson = request.get_json()
    effect = FeatService.getFeatEffectFromJSON(requestJson)
    effect.featId = id
    added = FeatService.addEffect(effect)
    if added:
        return OK(added)
    else:
        return BadRequest("Could not add effect to feat.")

@feats.route("/feats/effects/<effectId>", methods = ['DELETE'])
@isAdmin
def addFeatEffect(effectId: str):
    success = FeatService.deleteFeatEffect(effectId)
    if success:
        return OK(success)
    else:
        return BadRequest("Could not remove effect from feat.")
    
@feats.route("/feats/<id>", methods = ['DELETE'])
@isAdmin
def deleteFeat(id: str):
    deleted, errors = FeatService.delete(id)
    if deleted:
        return OK(deleted)
    else:
        return BadRequest(errors)
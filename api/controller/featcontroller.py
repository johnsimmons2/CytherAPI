
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.classes import Feat, Race
from api.service.dbservice import FeatService


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
@isAuthorized
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
@isAuthorized
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
    
    
@feats.route("/feats/<id>", methods = ['DELETE'])
@isAuthorized
@isAdmin
def deleteFeat(id: str):
    deleted, errors = FeatService.delete(id)
    if deleted:
        return OK(deleted)
    else:
        return BadRequest(errors)
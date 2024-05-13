from flask import Blueprint, request
from CytherAPI.api.controller.controller import validRequestDataFor
from api.model.spells import SpellComponents, Spells
from api.model.spellbook import Spellbook, SpellbookKnowledge
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.controller import OK, UnAuthorized, BadRequest, Posted, HandleGet
from api.service.dbservice import SpellService, SpellbookService

spells = Blueprint('spells', __name__)

@spells.route("/spells", methods = ['GET'])
@isAuthorized
def get():
  return HandleGet(SpellService.getAll())

@spells.route("/spells", methods = ['POST'])
@isAuthorized
@isAdmin
def createSpell():
  if request.get_json() is None:
    return BadRequest('No JSON was provided for the spell.')

  spellJson = request.get_json()
  if validRequestDataFor(spellJson, Spells):
    createdId, errors = SpellService.createSpell(Spells(**spellJson))
    if createdId > 0:
      return Posted({"spellId": createdId})
    else:
      return BadRequest(errors)
  return BadRequest("This was bad data")

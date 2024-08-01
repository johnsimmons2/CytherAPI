from flask import Blueprint, request
from api.controller.controller import validRequestDataFor, BadRequest, Posted, HandleGet
from api.model.spells import SpellComponents, Spells
from api.model.spellbook import Spellbook, SpellbookKnowledge
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.decorator.validatepostbody import validate_post_body
from api.service.dbservice import SpellService, SpellbookService

spells = Blueprint('spells', __name__)

@spells.route("/spells", methods = ['GET'])
@isAuthorized
def get():
  return HandleGet(SpellService.getAll())

@spells.route("/spells/<id>", methods = ['GET'])
@isAuthorized
def getById(id: int):
  return HandleGet(SpellService.get(id))

@spells.route("/spells", methods = ['POST'])
@isAuthorized
@isAdmin
@validate_post_body(validRequestDataFor, Spells)
def createSpell(spell: Spells, nestedData: dict):
  components = SpellComponents(**nestedData['components'])
  createdId, errors = SpellService.createSpell(spell, components)
  if createdId > 0:
    return Posted({"spellId": createdId})
  else:
    return BadRequest(errors)

@spells.route("/spells/<id>", methods = ['PATCH'])
@isAuthorized
@isAdmin
@validate_post_body(validRequestDataFor, Spells)
def updateSpell(spell: Spells, nestedData: dict, id: int):
  components = SpellComponents(**nestedData['components'])
  components.spellId = id
  spell.id = id

  createdId, errors = SpellService.updateSpell(spell, components)
  if createdId > 0:
    return Posted({"spellId": createdId})
  else:
    return BadRequest(errors)

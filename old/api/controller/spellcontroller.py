from flask import Blueprint, request
from api.controller.controller import validRequestDataFor, BadRequest, Posted, HandleGet
from api.model.spell import Spell
from api.model.spellbook import Spellbook, SpellbookSpell
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.service.repo.spellservice import SpellService
from api.service.repo.spellbookservice import SpellbookService

spells = Blueprint('spells', __name__)

@spells.route("/spells", methods = ['GET'])
@isAuthorized
def get():
  return HandleGet(SpellService.getAll())

@spells.route("/spells/<id>", methods = ['GET'])
@isAuthorized
def getById(id: int):
  return HandleGet(SpellService.get(id))

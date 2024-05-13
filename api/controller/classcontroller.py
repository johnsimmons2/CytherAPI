
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted, HandleGet

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.classes import Race
from api.service.dbservice import ClassService


classes = Blueprint('classes', __name__)

@classes.route("/classes", methods = ['GET'])
@isAuthorized
def get():
    classes = ClassService.getAll()
    if classes is not None:
        if len(classes) > 0:
            return OK(classes)
        else:
            return NotFound("No classes could be found in the database.")
    else:
        return ServerError("The request to get classes returned None instead of an empty list.")


@classes.route("/classes/<id>", methods = ['GET'])
@isAuthorized
def getById(id):
    HandleGet(ClassService.get(id))

@classes.route("/classes/<id>/table", methods = ['GET'])
@isAuthorized
def getClassTable(id):
    HandleGet(ClassService.getClassTable(id))


@classes.route("/classes/<id>/table", methods = ['PATCH'])
@isAdmin
@isAuthorized
def updateClassTable(id):
    if request.get_json() is None:
        return BadRequest('No class table was provided or the input was invalid.')
    classTableJson = request.get_json()
    success, errors = ClassService.updateClassTable(id, classTableJson)
    if success:
        return Posted(id)
    return BadRequest(errors)

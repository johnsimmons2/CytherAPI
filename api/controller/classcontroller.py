
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted, HandleGet

from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.classes import Class, Race
from api.service.repo.classservice import ClassService


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

@classes.route("/classes/<id>/subclasses", methods = ['GET'])
@isAuthorized
def getSubs(id: str):
    classes = ClassService.getClassSubclasses(id)
    if classes is not None:
        if len(classes) > 0:
            return OK(classes)
        else:
            return NotFound("The class provided did not have any subclasses.")
    else:
        return ServerError("The request to get classes returned None instead of an empty list.")

@classes.route("/classes/<id>/subclasses", methods = ['POST'])
@isAuthorized
def createSubclass(id: str):
    classes = ClassService.getClassSubclasses(id)
    if classes is not None:
        if len(classes) > 0:
            return OK(classes)
        else:
            return NotFound("The class provided did not have any subclasses.")
    else:
        return ServerError("The request to get classes returned None instead of an empty list.")

@classes.route("/classes", methods = ['POST'])
@isAuthorized
@isAdmin
def post():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the class.')

    classJson = request.get_json()
    if 'subclassIds' in classJson:
        subclasses = _get_subclasses_from_json(classJson)

        if type(subclasses) is str:
            return BadRequest(subclasses)
        del classJson['subclassIds']

    if validRequestDataFor(classJson, Class):
        created, errors = ClassService.createClass(Class(**classJson))
        if created:
            return Posted(created)
        else:
            return BadRequest(errors)
    else:
        return BadRequest('The JSON provided was not valid for the Class.')


@classes.route("/classes/<id>", methods = ['DELETE'])
@isAuthorized
@isAdmin
def delete(id: str):
    deleted, errors = ClassService.delete(id)
    if deleted:
        return OK(deleted)
    else:
        return BadRequest(errors)

@classes.route("/classes/<id>", methods = ['PATCH'])
@isAuthorized
@isAdmin
def patch(id: str):
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the feat.')

    classJson = request.get_json()
    subclasses = []

    if 'subclassIds' in classJson:
        subclasses = _get_subclasses_from_json(classJson)

        if type(subclasses) is str:
            return BadRequest(subclasses)
        del classJson['subclassIds']

    if validRequestDataFor(classJson, Class):
        feat = Class(**classJson)
        feat.id = id
        updated, errors = ClassService.update(int(id), feat)
        if updated:
            return OK(updated)
        else:
            return BadRequest(errors)
    else:
        return BadRequest('The JSON provided was not valid for the Class.')


def _get_subclasses_from_json(json):
    subclasses = []

    for sub in json['subclassIds']:
        print(json['subclassIds'])
        if type(sub) is not int:
            return 'Feat must be supplied as an ID for existing feat.'
        foundSub = ClassService.getSubclass(str(sub))
        if not foundSub:
            return 'Was not able to get a Subclass with ID: ' + str(sub)
        subclasses.append(foundSub)

    return subclasses

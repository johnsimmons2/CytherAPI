
from flask import Blueprint, request
from api.controller.controller import OK, BadRequest, NotFound, ServerError, validRequestDataFor, Posted

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
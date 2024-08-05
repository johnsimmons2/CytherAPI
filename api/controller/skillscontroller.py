
from flask import Blueprint, request
from api.controller.controller import OK, NotFound, ServerError

from api.decorator.auth.authdecorators import isAuthorized
from api.service.repo.skillservice import SkillService


skills = Blueprint('skills', __name__)

@skills.route("/skills", methods = ['GET'])
@isAuthorized
def get():
    skills = SkillService.getAll()
    if skills is not None:
        if len(skills) > 0:
            return OK(skills)
        else:
            return NotFound("No skills could be found in the database.")
    else:
        return ServerError("The request to get skills returned None instead of an empty list.")

# CREATE SKILLS
# @race.route("/skills", methods = ['POST'])
# @isAuthorized
# @isAdmin
# def createRace():
#     pass

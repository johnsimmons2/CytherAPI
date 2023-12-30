import json
from flask import Blueprint, request, jsonify
from api.controller import OK, BadRequest, Posted
from api.service.ext_dbservice import Ext_ContentService
from api.service.jwthelper import create_token
from api.loghandler.logger import Logger
import api.service.jwthelper as jwth


ext_content = Blueprint('ext_content', __name__)

@ext_content.route("/ext", methods = ['GET'])
def getAll():
    result = Ext_ContentService.getAll()
    return OK(result)

@ext_content.route("/ext/key", methods = ['GET'])
def getAllLikeKey():
    keyLike = request.args.get('like')
    if keyLike is None:
        return BadRequest('No key was provided.')

    result = Ext_ContentService.getAllLikeKey(keyLike)
    return OK(result)

@ext_content.route("/ext/<id>", methods = ['GET'])
def get(id: str):
    result = Ext_ContentService.get(id)
    if result is None:
        return BadRequest('No content was found with that ID.')
    return OK()

@ext_content.route("/ext/key/<key>", methods = ['GET'])
def getByKey(key: str):
    result = Ext_ContentService.getByKey(key)
    if result is None:
        return BadRequest('No content was found with that key.')
    return OK(result)

@ext_content.route("/ext", methods = ['POST'])
def update():
    if request.get_json() is None:
        return BadRequest('No content was provided or the input was invalid.')
    
    contentId = request.args.get('id')

    Ext_ContentService.update(contentId, request.get_json())
    return Posted(Ext_ContentService.getByKey(request.get_json()['key']))
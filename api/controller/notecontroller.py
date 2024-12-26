from flask import Blueprint, request

from api.controller.controller import OK, BadRequest, NotFound, Posted, validRequestDataFor
from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.note import Note
from api.model.user import User
from api.service.dbservice import UserService
from api.service.jwthelper import decode_token, get_access_token
from api.service.repo.campaignservice import CampaignService
from api.service.repo.noteservice import NoteService


notes = Blueprint('notes', __name__)

# NOTE: auth decorators must come after the route definition
@notes.route("/notes", methods = ['GET'])
@isAuthorized
def get():
    token = decode_token(get_access_token())
    username = token['username']
    user: User = UserService.getByUsername(username)
    
    for role in user.roles:
        if role.level == 0:
            notes = NoteService.getAll()
            if notes is not None:
                if len(notes) > 0:
                    return OK(notes)
                else:
                    return NotFound("No notes could be found in the database.")
        
    notes = NoteService.getAllForUser(user.id)
    if notes is not None:
        if len(notes) > 0:
            return OK(notes)
        else:
            return NotFound("No notes could be found for the given user.")

@notes.route("/notes", methods = ['POST'])
@isAuthorized
def createUserNote():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the note.')
    
    noteJson = request.get_json()
    
    token = decode_token(get_access_token())
    username = token['username']
    user: User = UserService.getByUsername(username)
        
    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        note.userId = user.id
        note.creator = user
        createNote(note)

@notes.route("/notes/campaign", methods = ['POST'])
@isAdmin
def createCampaignWideNote():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the note.')
    
    noteJson = request.get_json()
    
    token = decode_token(get_access_token())
    campaign = CampaignService.get(noteJson['campaignId'])

    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        createNote(note)
        
@notes.route("/notes/<id>", methods = ['POST'])
@isAuthorized
def createCharacterNote():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the note.')
    
    noteJson = request.get_json()
    
    token = decode_token(get_access_token())
    character = UserService.getCharacter(noteJson['characterId'])
    
    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        note.character = character
        createNote(note)

def createNote(note: Note):
    noteJson = request.get_json()
    if validRequestDataFor(noteJson, Note):
        created, errors = NoteService.create(note)
        if created:
            return Posted(created)
        else:
            return BadRequest(errors)
        
@notes.route("/notes/<id>", methods = ['PATCH'])
@isAuthorized
def updateNote():
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    
    noteJson = request.get_json()
    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        updated = NoteService.update(note)
        if updated:
            return OK(updated)
        else:
            return BadRequest("The note could not be updated.")
    else:
        return BadRequest("The JSON provided was not valid for the note.")

@notes.route("/notes/<id>/share", methods = ['POST'])
def shareNote():
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    
    noteJson = request.get_json()
    playerIds = noteJson['shared_users']
    if validRequestDataFor(noteJson, Note):
        note = NoteService.get(noteJson['noteId'])
        if note:
            NoteService.shareNote(note, playerIds)
        else:
            return NotFound("The note could not be found.")
    else:
        return BadRequest("The JSON provided was not valid for the note.")
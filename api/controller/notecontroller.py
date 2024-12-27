from flask import Blueprint, request

from api.controller.controller import OK, BadRequest, NotFound, Posted, validRequestDataFor
from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.model.campaign import Campaign
from api.model.character import Character
from api.model.note import Note
from api.model.user import User
from api.service.dbservice import UserService
from api.service.jwthelper import decode_token, get_access_token
from api.service.repo.campaignservice import CampaignService
from api.service.repo.characterservice import CharacterService
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
        return createNote(note)

@notes.route("/notes/campaign", methods = ['POST'])
@isAdmin
def createCampaignWideNote():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the note.')
    
    noteJson = request.get_json()
    
    token = decode_token(get_access_token())
    if not 'campaignId' in noteJson:
        return BadRequest("No campaign ID was provided for the note.")
    campaign: Campaign = CampaignService.get(noteJson['campaignId'])

    if not campaign:
        return NotFound("The campaign could not be found.")
    
    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        note.userId = None
        note.campaignId = campaign.id
        return createNote(note)
        
@notes.route("/notes/character", methods = ['POST'])
@isAuthorized
def createCharacterNote():
    if request.get_json() is None:
        return BadRequest('No JSON was provided for the note.')
    
    noteJson = request.get_json()
    
    token = decode_token(get_access_token())
    character: Character = CharacterService.get(noteJson['characterId'])
    
    if not character:
        return NotFound("The character could not be found.")
    
    if validRequestDataFor(noteJson, Note):
        note = Note(**noteJson)
        note.creator = UserService.getByUsername(token['username'])
        note.characterId = character.id
        note.character = character
        return createNote(note)

def createNote(note: Note):
    created = NoteService.create(note)
    if created:
        return Posted(created)
    else:
        return BadRequest("The note could not be created.")
        
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
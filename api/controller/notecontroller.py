from flask import Blueprint, request

from api.controller.controller import OK, BadRequest, Forbidden, NotFound, Posted, validRequestDataFor
from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.loghandler.logger import Logger
from api.model.campaign import Campaign
from api.model.character import Character
from api.model.note import Note
from api.model.user import User
from api.service.dbservice import RoleService, UserService
from api.service.jwthelper import decode_token, get_access_token
from api.service.repo.campaignservice import CampaignService
from api.service.repo.characterservice import CharacterService
from api.service.repo.noteservice import NoteService


notes = Blueprint('notes', __name__)

# NOTE: auth decorators must come after the route definition
'''
    Returns all notes for the user, or all notes period if the token is an admin.
'''
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
        
    notes = NoteService.getAllForUser(user.id) # Make sure this gets all the shared notes too
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
        
    try:
        note = Note(**noteJson)
        note.userId = user.id
        note.creator = user
        return _createNote(note)
    except:
        return BadRequest("The note could not be created, Invalid Data.")

'''
    Shortcut route for admins only.
    Creates a note that has no directory root and is tied to the campaign specified.
'''
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
    
    try:
        note = Note(**noteJson)
        note.userId = None
        note.campaignId = campaign.id
        return _createNote(note)
    except Exception as e:
        return BadRequest("The note could not be created, Invalid Data.")

def _createNote(note: Note):
    created = NoteService.create(note)
    if created:
        return Posted(created)
    else:
        return BadRequest("The note could not be created.")
        
@notes.route("/notes/<id>", methods = ['PATCH'])
@isAuthorized
def updateNote(id: str):
    # TODO: Make sure only admins can update all notes, other users can only update what they OWN
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    
    noteJson = request.get_json()
    
    isadmin = False
    ownsnote = False
    
    
    newNote = Note()
    if 'description' in noteJson:
        newNote.description = noteJson['description']
    
    if 'directory' in noteJson:
        newNote.directory = noteJson['directory']
    
    if 'name' in noteJson:
        newNote.name = noteJson['name']
        
    updated = NoteService.update(id, newNote)
    if updated:
        return OK(updated)
    else:
        return BadRequest("The note could not be updated.")

@notes.route("/notes/<id>", methods = ['GET'])
@isAuthorized
def getNoteById(id: str):
    noteId = id
    # TODO: Make sure only admins can get all notes, other users can only get what is shared!
    note = NoteService.get(noteId)
    user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
    if note is None:
        return NotFound("The note could not be found by that ID.")
    
    is_admin = False
    for role in user.roles:
        if role.level == 0:
            is_admin = True
            break
    if note.active == False:
        if is_admin:
            return OK(note)
        else:
            return Forbidden("You do not have permission to view this note.")
    else:
        if note.creator is None:
            return OK(note)
        if note.creator.id != user.id and not is_admin:
            return Forbidden("You do not have permission to view this note.")
    return OK(note)
        
    
@notes.route("/notes/<id>", methods = ['DELETE'])
@isAuthorized
def deleteNoteById(id: str):
    noteId = id
    # TODO: Make sure only admins can get all notes, other users can only get what is shared!
    note = NoteService.get(noteId)
    user = UserService.getByUsername(decode_token(get_access_token())['username'])
    
    if note is None:
        return NotFound("The note could not be found by that ID.")
    
    is_admin = False
    if note.creator is None:
        for role in user.roles:
            if role.level == 0:
                is_admin = True
                break
        if is_admin:
            NoteService.disableNote(note)
            return OK(note)
        else:
            return Forbidden("You do not have permission to delete this note.")
    else:
        if note.creator.id != user.id:
            return Forbidden("You do not have permission to delete this note.")
        if note:
            NoteService.disableNote(note)
            return OK(note)

@notes.route("/notes/share", methods = ['POST'])
def shareNote():
    # Only let admins share "any" note
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    
    noteJson = request.get_json()
    if not 'noteId' and not 'directory' in noteJson:
        return BadRequest("No note ID or directory was provided for the share request.")
    
    note: Note = None
    
    if not 'userIds' in noteJson:
        if not 'campaignId' in noteJson:
            return BadRequest("No user IDs, directory, or campaign ID was provided for the note.")
        else:
            campaignId = noteJson['campaignId']
            note = NoteService.shareNoteToCampaign(campaignId, noteJson['noteId'])
    else:
        userIds = noteJson['userIds']
        if not 'directory' in noteJson:
            note = NoteService.shareNote(userIds, noteJson['noteId'])
        else:
            note = NoteService.shareNoteDirectory(userIds, noteJson['directory'])
    Logger.debug(note)
    if note:
        return OK(note)
    else:
        BadRequest("The note or directory could not be shared.")
        
@notes.route("/notes/directory", methods = ['GET'])
@isAuthorized
def getNotesByDirectory():
    if request.args.get('d') is None:
        if request.args.get('u') is None:
            return BadRequest("No directory (d) or username (u) was provided for the notes.")
        username = request.args.get('u')
        user: User = UserService.getByUsername(username)
        notes = NoteService.getNotesByUserForDirectory(user.id)
    else:
        directory = request.args.get('d')
        notes = NoteService.getNotesByDirectory(directory)
        
    if notes is not None:
        if len(notes) > 0:
            return OK(notes)
        else:
            return NotFound("No notes could be found for the given directory.")
    else:
        return NotFound("No notes could be found.")
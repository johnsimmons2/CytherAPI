from flask import Blueprint, request

from api.controller.controller import OK, BadRequest, Conflict, Forbidden, NotFound, Posted, validRequestDataFor
from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.loghandler.logger import Logger
from api.model.campaign import Campaign
from api.model.character import Character
from api.model.note import Note, Tag
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
        note = Note()
        if 'description' in noteJson:
            note.description = noteJson['description']
            
        if 'name' in noteJson:
            note.name = noteJson['name']
        else:
            return BadRequest("The note could not be created, missing name.")
        
        if 'directory' in noteJson:
            note.directory = noteJson['directory']
        else:
            note.directory = user.username + '/'
        
        note.userId = user.id
        note.creator = user
        
        if 'tags' in noteJson:
            foundTags = []
            for tag in noteJson['tags']:
                foundTag = NoteService.getTag(tag)
                if foundTag:
                    foundTags.append(foundTag)
            note.tags = foundTags
        
        return _createNote(note)
    except Exception as e:
        Logger.error(e)
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
    
    if not 'campaignId' in noteJson:
        return BadRequest("No campaign ID was provided for the note.")
    campaign: Campaign = CampaignService.get(noteJson['campaignId'])

    if not campaign:
        return NotFound("The campaign could not be found.")
    
    try:
        note = Note()
        if 'description' in noteJson:
            note.description = noteJson['description']
            
        if 'name' in noteJson:
            note.name = noteJson['name']
        else:
            return BadRequest("The note could not be created, missing name.")
        
        if 'directory' in noteJson:
            note.directory = campaign.name + '/' + noteJson['directory']
        else:
            note.directory = campaign.name
        note.campaign = campaign
        
        return _createNote(note)
    except Exception as e:
        Logger.error(e)
        return BadRequest("The note could not be created, Invalid Data.")

@notes.route("/notes/<id>/tag/<tagId>", methods = ['POST'])
@isAuthorized
def addTagToNote(id: str, tagId: str):
    isadmin = False
    ownsnote = False
    user = None
    note = NoteService.get(id)
    if note is None:
        return NotFound("The note could not be found by that ID.")
    
    tag = NoteService.getTag(tagId)
    if tag is None:
        return NotFound("The tag could not be found by that ID.")
    
    noteHasTag = tag in note.tags
    if noteHasTag:
        return Conflict("The note already has this tag.")
    
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        ownsnote = NoteService.get(id).userId == user.id
    except:
        return BadRequest("The note could not be updated, there was an issue with the token provided.")
    
    for role in user.roles:
        if role.level == 0:
            isadmin = True
            break
    
    if not isadmin and not ownsnote:
        return Forbidden("You do not have permission to update this note.")
    
    result = NoteService.tagNote(note, tag)
    if result:
        return OK(result)
    return NotFound("The note or tag could not be found.")

@notes.route("/notes/tag/icons", methods = ['GET'])
@isAuthorized
def getAllIconOptions():
    icons = NoteService.getTagIconOptions()
    if icons:
        return OK(icons)
    return NotFound("No icons could be found.")

@notes.route("/notes/<id>/tag/<tagId>", methods = ['DELETE'])
@isAuthorized
def removeTagFromNote(id: str, tagId: str):
    isadmin = False
    ownsnote = False
    user = None
    note = NoteService.get(id)
    if note is None:
        return NotFound("The note could not be found by that ID.")
    
    tag = NoteService.getTag(tagId)
    if tag is None:
        return NotFound("The tag could not be found by that ID.")
    
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        ownsnote = NoteService.get(id).userId == user.id
    except:
        return BadRequest("The note could not be updated, there was an issue with the token provided.")
    
    for role in user.roles:
        if role.level == 0:
            isadmin = True
            break
    
    if not isadmin and not ownsnote:
        return Forbidden("You do not have permission to update this note.")
    
    result = NoteService.unTagNote(note, tag)
    if result:
        return OK(result)
    return NotFound("The note or tag could not be found.")

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
    user = None
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        ownsnote = NoteService.get(id).userId == user.id
    except:
        return BadRequest("The note could not be updated, there was an issue with the token provided.")
    
    for role in user.roles:
        if role.level == 0:
            isadmin = True
            break
    
    if not isadmin and not ownsnote:
        return Forbidden("You do not have permission to update this note.")
    
    newNote = Note()
    if 'description' in noteJson:
        newNote.description = noteJson['description']
    
    if 'directory' in noteJson:
        newNote.directory = noteJson['directory']
    
    if 'name' in noteJson:
        newNote.name = noteJson['name']
    
    if 'tags' in noteJson:
        foundTags = []
        for tag in noteJson['tags']:
            foundTag = NoteService.getTag(tag)
            if foundTag:
                foundTags.append(foundTag)
        newNote.tags = foundTags
    
    try:
        updated = NoteService.update(id, newNote)
        if updated:
            return OK(updated)
    except Exception as e:
        Logger.error(e)
    return BadRequest("The note could not be updated.")

@notes.route("/notes/<id>", methods = ['GET'])
@isAuthorized
def getNoteById(id: str):
    noteId = id
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
            Logger.debug(f"{note.shared_users}, {user.id}")
            if not NoteService.checkIfNoteIsShared(note, user):
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
    for role in user.roles:
            if role.level == 0:
                is_admin = True
                break
            
    if note.creator is None:
        if is_admin:
            NoteService.deleteNote(note)
            return OK(note)
        else:
            return Forbidden("You do not have permission to delete this note.")
    else:
        if is_admin:
                NoteService.deleteNote(note)
                return OK(note)
        elif note.creator.id != user.id:
            return Forbidden("You do not have permission to delete this note.")
        NoteService.disableNote(note)
        return OK(note)

@notes.route("/notes/share/tag/<tagId>/status", methods = ['GET'])
@isAuthorized
def getTagShares(tagId: str):
    tag = None
    user = None
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        tag = NoteService.getTag(tagId)
    except:
        return BadRequest("No tag or user was found attached to request.")
    
    return OK(NoteService.getTagSharedUsers(tag.id, user.id))
    

@notes.route("notes/share/directory/status", methods = ['GET'])
@isAuthorized
def getDirectoryShares():
    user = None
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
    except:
        return BadRequest("No tag or user was found attached to request.")
    
    return OK(NoteService.getDirectorySharedUsers(user.id))

@notes.route("/notes/share/tag/<tagId>", methods = ['POST'])
@isAuthorized
def shareTag(tagId: str):
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag share request.")
    
    tag = None
    user = None
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        tag = NoteService.getTag(tagId)
    except:
        return BadRequest("The tag could not be shared, there was an issue with the token provided.")
    
    shareJson = request.get_json()
    
    if 'userIds' not in shareJson:
        return BadRequest("No user IDs were provided for the tag share request.")
    
    userIds = shareJson['userIds']
    result = []
    for otherId in userIds:
        sharedTag = NoteService.shareTag(tag.id, user.id, otherId)
        if sharedTag:
            result.append(sharedTag)
    
    if len(result) == 0:
        return BadRequest("The tag could not be shared with the specified user IDs.")
    return Posted(result)

@notes.route("/notes/unshare/tag/<tagId>", methods = ['DELETE'])
@isAuthorized
def unShareTag(tagId: str):
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag un-share request.")
    
    tag = None
    user = None
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        tag = NoteService.getTag(tagId)
    except:
        return BadRequest("The tag could not be un-shared, there was an issue with the token provided.")
    
    shareJson = request.get_json()
    
    if 'userIds' not in shareJson:
        return BadRequest("No user IDs were provided for the tag un-share request.")
    
    userIds = shareJson['userIds']
    result = []
    for otherId in userIds:
        sharedTag = NoteService.unShareTag(tag.id, user.id, otherId)
        if sharedTag:
            result.append(sharedTag)
    
    if len(result) == 0:
        return BadRequest("The tag could not be un-shared with the specified user IDs.")
    return Posted(result)

@notes.route("/notes/tag", methods = ['GET'])
@isAuthorized
def getTags():
    tags = NoteService.getAllTags()
    if tags is not None:
        if len(tags) > 0:
            return OK(tags)
        else:
            return NotFound("No tags could be found in the database.")
    else:
        return NotFound("No tags could be found.")

@notes.route("/notes/tag", methods = ['POST'])
@isAuthorized
def createTag():
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag.")
    user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        
    admin = False
    for role in user.roles:
            if role.level == 0:
                admin = True
                break
            
    tagJson = request.get_json()
    tag = Tag()
    if not 'name' in tagJson:
        return BadRequest("No name was provided for the tag.")
    else:
        tag.name = tagJson['name']
        
    if not 'description' in tagJson:
        return BadRequest("No description was provided for the tag.")
    else:
        tag.description = tagJson['description']
    if not admin:
        tag.userId = user.id
    
    if 'color' in tagJson:
        tag.color = tagJson['color']
    
    if 'icon' in tagJson:
        tag.icon = tagJson['icon']
    
    createdTag = NoteService.createTag(tag)
    if createdTag:
        return Posted(createdTag)
    return BadRequest("The tag could not be created.")

@notes.route("/notes/tag/<tagId>", methods = ['PATCH'])
@isAuthorized
def updateTag(tagId: str):
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag.")
    user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
    tag: Tag = NoteService.getTag(tagId)
    
    admin = False
    for role in user.roles:
            if role.level == 0:
                admin = True
                break
    if not tag:
        return NotFound("The tag could not be found by that ID.")
    if not admin and tag.userId != user.id:
        return Forbidden("You do not have permission to update this tag.")
    
    tagJson = request.get_json()
    if 'name' in tagJson:
        tag.name = tagJson['name']
    if 'description' in tagJson:
        tag.description = tagJson['description']
    if 'color' in tagJson:
        tag.color = tagJson['color']
    if 'icon' in tagJson:
        tag.icon = tagJson['icon']
    success = NoteService.updateTag(tag)
    if success:
        return OK(success)
    return BadRequest("The tag could not be updated, verify a tag with the given name does not already exist.")

@notes.route("/notes/tag/<tagId>", methods = ['GET'])
@isAuthorized
def getTagById(tagId: str):
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag.")
    tag = NoteService.getTag(tagId)
    if tag:
        return OK(tag)
    return NotFound("The tag could not be found by that ID.")

@notes.route("/notes/tag/<tagId>", methods = ['DELETE'])
@isAdmin
def deleteTagById(tagId: str):
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the tag.")
    tag = NoteService.get(tagId)
    user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        
    admin = False
    for role in user.roles:
            if role.level == 0:
                admin = True
                break
    
    if tag:
        if admin or tag.userId == user.id:
            NoteService.deleteTag(tagId)
            return OK()
        else:
            return Forbidden("You do not have permission to delete this tag.")
    return NotFound("The tag could not be found by that ID.")

@notes.route("/notes/share", methods = ['POST'])
@isAuthorized
def shareNote():
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    isadmin = False
    ownsnote = False
    user = None
    existingNoteId = None
    
    # noteId is required for all of the shares except for directory shares.
    noteJson = request.get_json()
    if not 'noteId' in noteJson:
        if not 'directory' in noteJson:
            return BadRequest("No note ID, or directory was provided for the share request.")
        # TODO: Check if user owns a note within this directory anyway.
        ownsnote = True
    else:
        existingNoteId = noteJson['noteId']
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        if (existingNoteId):
            ownsnote = NoteService.get(existingNoteId).userId == user.id
    except:
        return BadRequest("The note could not be updated, there was an issue with the token provided.")
    
    for role in user.roles:
        if role.level == 0:
            isadmin = True
            break
    
    if not isadmin and not ownsnote:
        return Forbidden("You do not have permission to share this note.")
    
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
            note = NoteService.shareNoteDirectory(user.id, userIds, noteJson['directory'])
    if note:
        return OK(note)
    else:
        BadRequest("The note or directory could not be shared.")

@notes.route("/notes/unshare", methods = ['DELETE'])
@isAuthorized
def unShare():
    if request.get_json() is None:
        return BadRequest("No JSON was provided for the note.")
    isadmin = False
    ownsnote = False
    user = None
    existingNoteId = None
    
    # noteId is required for all of the shares except for directory shares.
    noteJson = request.get_json()
    if not 'noteId' in noteJson:
        if not 'directory' in noteJson:
            return BadRequest("No note ID, or directory was provided for the un-share request.")
        # TODO: Check if user owns a note within this directory anyway.
        ownsnote = True
    else:
        existingNoteId = noteJson['noteId']
    try:
        user: User = UserService.getByUsername(decode_token(get_access_token())['username'])
        if (existingNoteId):
            ownsnote = NoteService.get(existingNoteId).userId == user.id
    except:
        return BadRequest("The note could not be updated, there was an issue with the token provided.")
    
    for role in user.roles:
        if role.level == 0:
            isadmin = True
            break
    
    if not isadmin and not ownsnote:
        return Forbidden("You do not have permission to un-share this note.")
    
    note: Note = None
    if not 'userIds' in noteJson:
        if not 'campaignId' in noteJson:
            return BadRequest("No user IDs, directory, or campaign ID was provided for the note.")
        else:
            note = NoteService.unShareNoteFromCampaign(noteJson['noteId'])
    else:
        userIds = noteJson['userIds']
        if not 'directory' in noteJson:
            note = NoteService.unShareNote(userIds, noteJson['noteId'])
        else:
            note = NoteService.unShareNoteDirectory(user.id, userIds, noteJson['directory'])
    if note:
        return OK(note)
    else:
        BadRequest("The note or directory could not be un-shared.")

@notes.route("/notes/shared/<id>", methods = ['GET'])
@isAuthorized
def getSharedUsersByNoteId(id: str):
    noteId = id
    sharedUsers = NoteService.getSharedUsersByNoteId(noteId)
    if sharedUsers is not None:
        if len(sharedUsers) > 0:
            return OK(sharedUsers)
        else:
            return NotFound("No shared users could be found for the given note.")
    else:
        return NotFound("No shared users could be found.")

@notes.route("/notes/shared/tag/<tagId>", methods = ['GET'])
@isAuthorized
def getSharedUsersByTagId(tagId: str):
    sharedUsers = NoteService.getSharedUsersByTagId(tagId)
    if sharedUsers is not None:
        if len(sharedUsers) > 0:
            return OK(sharedUsers)
        else:
            return NotFound("No shared users could be found for the given note.")
    else:
        return NotFound("No shared users could be found.")

@notes.route("/notes/shared/directory/<directory>", methods = ['GET'])
@isAuthorized
def getSharedUsersByDirectory(directory: str):
    sharedUsers = NoteService.getSharedUsersByDirectory(directory)
    if sharedUsers is not None:
        if len(sharedUsers) > 0:
            return OK(sharedUsers)
        else:
            return NotFound("No shared users could be found for the given note.")
    else:
        return NotFound("No shared users could be found.")

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
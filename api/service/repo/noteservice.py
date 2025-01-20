from datetime import datetime, timezone
from api.model.campaign import Campaign, CampaignUsers
from api.model.character import Character
from api.model.note import Note, NoteSharedDirectories
from sqlalchemy.orm import Query
from api.model.user import Role, User, UserCharacters, UserRole
from extensions import db


class NoteService:
    query = Query(Note, db.session)
    
    @classmethod
    def get(cls, id: str) -> Note:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getAll(cls):
        return cls.query.all()
    
    @classmethod
    def getActive(cls):
        return cls.query.filter_by(active=True).all()
    
    @classmethod
    def getInactive(cls):
        return cls.query.filter_by(active=False).all()
    
    @classmethod
    def create(cls, note: Note):
        date_created = datetime.now(timezone.utc)
        newNote = Note()
        
        newNote.created = date_created
        newNote.updated = date_created
        newNote.active = True
        newNote.creator = note.creator
        newNote.userId = note.userId
        newNote.description = note.description
        newNote.name = note.name
        newNote.directory = note.directory
        
        db.session.add(newNote)
        db.session.commit()
        return note

    @classmethod
    def disableNote(cls, note: Note):
        note.active = False
        note.updated = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def getAllForUser(cls, id: str):
        is_admin = (
            db.session.query(UserRole)
                .join(Role, UserRole.roleId == Role.id)
                .filter(UserRole.userId == id, Role.level == 0)
                .count() > 0
        )
        
        created_by = cls.query.filter_by(userId=id)
        shared_with = cls.query.filter(Note.shared_users.any(id=id))
        character_notes = (
            cls.query
            .join(UserCharacters, UserCharacters.characterId == Note.characterId)
            .join(Character, Character.id == UserCharacters.characterId)
            .filter(UserCharacters.userId == id)
        )
        campaign_notes = (
            cls.query
            .join(CampaignUsers, CampaignUsers.userId == id)
            .filter(CampaignUsers.userId == id)
        )
        
        shared_with_directories = (
            cls.query
            .filter(Note.directory.in_(
                db.session.query(NoteSharedDirectories.directory)
                .filter(NoteSharedDirectories.userId == id)
            ))
        )
        
        query = created_by.union(shared_with, character_notes, campaign_notes, shared_with_directories)
        
        if not is_admin:
            query = query.filter(Note.active == True)
        return query.all()
    
    @classmethod
    def update(cls, id: str, note: Note):
        foundNote = cls.get(id)
        if foundNote:
            if note.name:
                foundNote.name = note.name
            if note.description:
                foundNote.description = note.description
            if note.active:
                foundNote.active = note.active
            foundNote.updated = datetime.now(timezone.utc)
            db.session.commit()
            return foundNote
        return None

    @classmethod
    def shareNote(cls, note: Note, userIds: list[int]):
        users = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return None
        
        current_user_ids = {user.id for user in note.shared_users} if note.shared_users else set()
        new_users = [user for user in users if user.id not in current_user_ids]
        
        if new_users:
            if not note.shared_users:
                note.shared_users = new_users
            else:
                note.shared_users.extend(new_users)
            
            note.updated = datetime.now(timezone.utc)
            db.session.commit()
        return note
    
    @classmethod
    def getNotesInDirectory(cls, directory: str):
        # Gets only the notes within the directory, not within the subdirectories.
        notesWithinDir = cls.query.filter(Note.directory.like(f"{directory}")).all()
        return notesWithinDir
    
    @classmethod
    def getNotesByDirectory(cls, directory: str):
        # This method gets ALL notes including notes in subdirectories, and maps them to a dictionary.
        grouped_notes = {}
        notes: list[Note] = cls.query.filter(Note.directory.like(f"{directory}%")).all()
        for note in notes:
            relative_path = note.directory[len(directory):] if directory else note.directory
            immediate_dir = relative_path.split('/')[0]
            full_dir = f"{directory}{immediate_dir}"

            if full_dir not in grouped_notes:
                grouped_notes[full_dir] = []
            grouped_notes[full_dir].append(note)

        return grouped_notes
    
    @classmethod
    def getNotesByUserForDirectory(cls, userId: int):
        grouped_notes = {}
        notes: list[Note] = cls.query.filter(Note.userId == userId).all()
        for note in notes:
            relative_path = note.directory

            if relative_path not in grouped_notes:
                grouped_notes[relative_path] = []
            grouped_notes[relative_path].append(note)

        return grouped_notes
    
    
    @classmethod
    def shareNoteDirectory(cls, userIds: list[int], directory: str) -> list[Note]:
        users: list[User] = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return False
        
        for user in users:
            shared_directory = Query(NoteSharedDirectories, db.session).filter_by(userId=user.id, directory=directory).first()
            if not shared_directory:
                shared_directory = NoteSharedDirectories(userId=user.id, directory=directory)
                db.session.add(shared_directory)
        db.session.commit()
        return True
    
    @classmethod
    def shareNoteToCampaign(cls, campaignId: int, noteId: int):
        note = cls.get(noteId)
        if not note:
            return None
        campaign = Query(Campaign, db.session).filter_by(id=campaignId).first()
        if not campaign:
            return None
        note.campaign = campaign
        note.updated = datetime.now(timezone.utc)
        db.session.commit()
        return note
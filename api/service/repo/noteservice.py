from datetime import date
from typing import List
from api.model.campaign import CampaignUsers
from api.model.character import Character
from api.model.note import Note
from sqlalchemy.orm import Query
from api.model.user import User
from extensions import db


class NoteService:
    query = Query(Note, db.session)
    
    @classmethod
    def get(cls, id: str):
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
        note.created = date.today()
        note.updated = date.today()
        note.active = True
        db.session.add(note)
        db.session.commit()
        return note

    @classmethod
    def getAllForUser(cls, id: str):
        created_by = cls.query.filter_by(userId=id)
        shared_with = cls.query.filter(Note.shared_users.any(id=id))
        character_notes = cls.query.join(Character).filter(Character.userId == id)
        campaign_notes = cls.query.join(CampaignUsers).join(CampaignUsers.userId).filter(CampaignUsers.userId==id)
        
        return created_by.union(shared_with, character_notes, campaign_notes).all()
    
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
            foundNote.updated = date.today()
            db.session.add(foundNote)
            db.session.commit()
            return foundNote
        return None

    @classmethod
    def shareNote(cls, note: Note, userIds: List[int]):
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
            
        db.session.commit()
        return note
    
        
from datetime import datetime, timezone

from sqlalchemy import or_
from api.loghandler.logger import Logger
from api.model.campaign import Campaign, CampaignUsers
from api.model.character import Character
from api.model.enums import TagIcons
from api.model.note import Note, NoteSharedDirectories, NoteSharedUsers, Tag, TagSharedUsers
from sqlalchemy.orm import Query
from api.model.user import Role, User, UserCharacters, UserRole
from extensions import db


class NoteService:
    query = db.Query(Note, db.session)
    tagQuery = db.Query(Tag, db.session)
    sharedTagQuery = db.Query(TagSharedUsers, db.session)
    sharedUserQuery = db.Query(NoteSharedUsers, db.session)
    sharedDirectoryQuery = db.Query(NoteSharedDirectories, db.session)
    
    @classmethod
    def init_default_tags(cls):
        defaults = [
            Tag(name="General", description="General notes that don't fit into any other category.", color="F94144", icon=TagIcons.FOLDER.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Character", description="Notes about specific characters.", color="F3722C", icon=TagIcons.PERSON.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Quest", description="Quests, side-quests, and plot-hooks.", color="00ffcc", icon=TagIcons.FLAG.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Lore", description="History, lore, and world knowledge.", color="F9C74F", icon=TagIcons.BOOK.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Treasure", description="Wondrous treasures and artifacts, owned or sought after.", color="90BE6D", icon=TagIcons.DIAMOND.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Bestiary", description="Notes on creatures, beasts, monsters, and enemies.", color="9933AA", icon=TagIcons.PAW.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Rumor", description="Things heard while exploring and eavesdropping.", color="4D908E", icon=TagIcons.EAR.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="To-Do", description="Planned activities.", color="669999", icon=TagIcons.CHECKMARK.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="NPC", description="Notes on characters discovered within the world.", color="277DA1", icon=TagIcons.PERSON.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Events", description="Special events and encounters.", color="003366", icon=TagIcons.EARTH.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Reference", description="Tables, charts, lists, and information.", color="F15BB5", icon=TagIcons.READER.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Mechanic", description="Game mechanics and rules.", color="00cc00", icon=TagIcons.COG.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
            Tag(name="Discovery", description="Documents found or notes about new findings.", color="ff0606", icon=TagIcons.SEARCH.value, active=True, created=datetime.now(timezone.utc), updated=datetime.now(timezone.utc)),
        ]
        
        existing_by_name = {
            row[0] for row in db.session.query(Tag.name).all()
        }
        
        for ability in defaults:
            if ability.name not in existing_by_name:
                db.session.add(ability)

        db.session.commit()
        
    
    @classmethod
    def getSharedUsersByNoteId(cls, noteId: str) -> list[User]:
        note = cls.get(noteId)
        if not note:
            return None
        noteShares: list[NoteSharedUsers] = cls.sharedUserQuery.filter_by(noteId=note.id).all()
        users = []
        for share in noteShares:
            user = Query(User, db.session).filter_by(id=share.userId).first()
            if user:
                users.append(user)
        return users
    
    @classmethod
    def getSharedUsersByDirectory(cls, userId: str, directory: str) -> list[User]:
        directory = cls.normalizeDirectory(directory)
        directoryShares: list[NoteSharedDirectories] = cls.sharedDirectoryQuery.filter_by(userId=userId, directory=directory).all()
        users = []
        for share in directoryShares:
            user = Query(User, db.session).filter_by(id=share.sharedWithId).first()
            if user:
                users.append(user)
        return users
    
    @classmethod
    def getSharedUsersByTagId(cls, userId: str, tagId: str) -> list[User]:
        tag = cls.getTag(tagId)
        if not tag:
            return None
        tagShares: list[TagSharedUsers] = cls.sharedTagQuery.filter_by(tagId=tag.id, userId=userId).all()
        users = []
        for share in tagShares:
            user = Query(User, db.session).filter_by(id=share.sharedWithId).first()
            if user:
                users.append(user)
        return users
    
    @classmethod
    def getTagSharedUsers(cls, tagId: str, userId: str) -> list[TagSharedUsers]:
        return cls.sharedTagQuery.filter_by(tagId=tagId, userId=userId).all()
    
    @classmethod
    def getDirectorySharedUsers(cls, userId: str) -> list[NoteSharedDirectories]:
        return cls.sharedDirectoryQuery.filter_by(userId=userId).all()
    
    @classmethod
    def updateTag(cls, tag: Tag):
        foundTag = cls.getTag(tag.id)
        if not foundTag:
            return None
        
        if tag.name:
            foundTag.name = tag.name
        if tag.description:
            foundTag.description = tag.description
        if tag.color:
            foundTag.color = tag.color
        if tag.icon:
            foundTag.icon = tag.icon
        if tag.active:
            foundTag.active = tag.active
        foundTag.updated = datetime.now(timezone.utc)
        
        conflict = cls.tagQuery.filter(Tag.id != foundTag.id, Tag.name==foundTag.name).first()
        if conflict:
            return False
        
        db.session.commit()
        return foundTag
    
    @classmethod
    def getTagIconOptions(cls):
        options = []
        for icon in TagIcons:
            options.append(icon.value)
        return options
    
    @classmethod
    def get(cls, id: str) -> Note:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getTag(cls, tagId: str) -> Tag:
        return cls.tagQuery.filter_by(id=tagId).first()
    
    @classmethod
    def getTagByName(cls, name: str) -> Tag:
        return cls.tagQuery.filter_by(name=name).first()
    
    @classmethod
    def getAllTags(cls) -> list[Tag]:
        return cls.tagQuery.all()
    
    @classmethod
    def getNotesByTag(cls, tagId: str):
        return cls.query.filter(Note.tags.any(id=tagId)).all()
    
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
        
        # Make sure there is not a note with the exact same name in the same directory
        existing = cls.query.filter_by(name=note.name, directory=note.directory).first()
        if existing:
            return None
        
        if note.campaign:
            newNote.campaign = note.campaign
        newNote.created = date_created
        newNote.updated = date_created
        newNote.active = True
        newNote.userId = note.userId
        newNote.description = note.description
        newNote.name = note.name
        if note.tags is not None:
            newNote.tags = note.tags
        newNote.directory = cls.normalizeDirectory(note.directory)
        
        db.session.add(newNote)
        db.session.commit()
        db.session.flush()
        return newNote
    
    @classmethod
    def createTag(cls, tag: Tag):
        date_created = datetime.now(timezone.utc)
        newTag = Tag()
        
        existing = cls.tagQuery.filter_by(name=tag.name).first()
        if existing:
            return None
        
        newTag.created = date_created
        newTag.updated = date_created
        newTag.active = True
        newTag.name = tag.name
        newTag.description = tag.description
        newTag.color = tag.color
        newTag.icon = tag.icon
        if tag.userId:
            newTag.userId = tag.userId
        
        db.session.add(newTag)
        db.session.commit()
        db.session.flush()
        return tag
    
    @classmethod
    def deleteTag(cls, tag: Tag):
        db.session.delete(tag)
        db.session.commit()
        
    @classmethod
    def disableTag(cls, tag: Tag):
        tag.active = False
        tag.updated = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def deleteNote(cls, note: Note):
        db.session.query(NoteSharedUsers).filter_by(noteId=note.id).delete(synchronize_session=False)
        note.tags = []
        # Delete the note
        db.session.delete(note)
        db.session.commit()

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
        
        Logger.debug('Is admin: %s', is_admin)
        # Get notes the user created.
        created_by = cls.query.filter_by(userId=id)
        # Get notes explicitly shared with the user.
        shared_with = cls.query.filter(Note.shared_users.any(id=id))
        # Get notes on a character owned by the user.
        character_notes = (
            cls.query
            .join(UserCharacters, UserCharacters.characterId == Note.characterId)
            .join(Character, Character.id == UserCharacters.characterId)
            .filter(UserCharacters.userId == id)
        )
        # Get notes in a campaign the user is in.
        campaign_notes = (
            cls.query
            .join(CampaignUsers, CampaignUsers.campaignId == Note.campaignId)
            .filter(CampaignUsers.userId == id)
        )
        
        shared_dirs = (
            db.session.query(NoteSharedDirectories.directory)
            .filter(NoteSharedDirectories.userId == id)
            .all()
        )
        # shared_dirs is a list of tuples [(dir1,), (dir2,), ...], so flatten:
        shared_dir_list = [d[0] for d in shared_dirs]

        # Build an OR condition for each directory to include it and its subdirectories.
        dir_conditions = []
        for directory in shared_dir_list:
            # Match exact directory OR anything that starts with directory + '/'
            dir_conditions.append(Note.directory == directory)
            dir_conditions.append(Note.directory.like(f"{directory}/%"))

        # If there are no shared directories, the OR would be empty.
        # We'll handle that gracefully in the union below.
        if dir_conditions:
            shared_with_directories = cls.query.filter(or_(*dir_conditions))
        else:
            # No shared directories for this user.
            shared_with_directories = cls.query.filter(False)  # returns no results

        
        # Get the tags that are shared with the user, and notes via the shared tags.
        shared_tags = (
            cls.tagQuery
            .join(TagSharedUsers, TagSharedUsers.tagId == Tag.id)
            .filter(TagSharedUsers.sharedWithId == id)
            .all()
        )
        shared_tag_ids = [tag.id for tag in shared_tags]
        if shared_tag_ids:
            shared_notes_by_tags = cls.query.filter(Note.tags.any(Tag.id.in_(shared_tag_ids)))
        else:
            shared_notes_by_tags = cls.query.filter(False)
        
        query = created_by.union(shared_with, character_notes, campaign_notes, shared_with_directories, shared_notes_by_tags)
        
        if not is_admin:
            query = query.filter(Note.active == True)
        notes= query.all()
        
        for n in notes:
            Logger.debug(n.name)
        return notes
    
    @classmethod
    def checkIfNoteIsShared(cls, note: Note, user: User):
        # Check if the note is directly shared with the user.
        shared = cls.sharedUserQuery.filter_by(noteId=note.id, userId=user.id).first()

        # Check if any tag on the note is shared with the user.
        tag_ids = [tag.id for tag in note.tags]  # assuming note.tags exists and is a list of Tag objects
        tagShared = None
        if tag_ids:
            tagShared = cls.sharedTagQuery.filter(
                TagSharedUsers.tagId.in_(tag_ids),
                TagSharedUsers.sharedWithId == user.id
            ).first()

        # Check if the note's directory is shared with the user.
        dirShared = cls.sharedDirectoryQuery.filter_by(userId=user.id, directory=note.directory).first()

        Logger.debug(f"Shared: {shared}, TagShared: {tagShared}, DirShared: {dirShared}")
        return shared or tagShared or dirShared
    
    @classmethod
    def update(cls, id: str, note: Note):
        foundNote = cls.get(id)
        if not foundNote:
            return None
        
        if note.name:
            foundNote.name = note.name
        if note.description:
            foundNote.description = note.description
        if note.directory:
            foundNote.directory = cls.normalizeDirectory(note.directory)
        if note.active:
            foundNote.active = note.active
        foundNote.updated = datetime.now(timezone.utc)
        
        conflict = cls.query.filter(Note.id != foundNote.id,
                                    Note.name==foundNote.name, 
                                    Note.directory==foundNote.directory)
        if foundNote.userId:
            conflict = conflict.filter(Note.userId==foundNote.userId)
        if foundNote.characterId:
            conflict = conflict.filter(Note.characterId==foundNote.characterId)
        if foundNote.campaignId:
            conflict = conflict.filter(Note.campaignId==foundNote.campaignId)
        conflict = conflict.first()
        if conflict:
            raise ValueError("A note with that name already exists in that directory.")
        
        db.session.commit()
        return foundNote

    @classmethod
    def shareNote(cls, userIds: list[int], noteId: str):
        users: list[User] = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return None
        note = cls.get(noteId)
        if not note:
            return None
        current_user_ids = {user.id for user in note.shared_users} if note.shared_users else set()
        new_users = [user for user in users if user.id not in current_user_ids]
        
        if new_users:
            for user in new_users:
                shared_note = NoteSharedUsers()
                shared_note.noteId = note.id
                shared_note.userId = user.id
                shared_note.shareDate = datetime.now(timezone.utc)
                db.session.add(shared_note)
            
            note.updated = datetime.now(timezone.utc)
            db.session.commit()
        return note

    @classmethod
    def unShareNote(cls, userIds: list[int], noteId: str):
        users: list[User] = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return None
        
        note = cls.get(noteId)
        if not note:
            return None
        current_user_ids = {user.id for user in note.shared_users} if note.shared_users else set()
        if len(current_user_ids) == 0:
            return None
        
        for user in userIds:
            if user in current_user_ids:
                current_user_ids.remove(user)
                shared_note = cls.sharedUserQuery.filter_by(noteId=note.id, userId=user).first()
                db.session.delete(shared_note)
        note.updated = datetime.now(timezone.utc)
        db.session.commit()
        return note

    @classmethod
    def tagNote(cls, note: Note, tag: Tag):
        note.tags.append(tag)
        note.updated = datetime.now(timezone.utc)
        db.session.commit()
        return note
    
    @classmethod
    def unTagNote(cls, note: Note, tag: Tag):
        note.tags.remove(tag)
        note.updated = datetime.now(timezone.utc)
        db.session.commit()
        return note
    
    # A user can share notes under a tag whether they made the tag or not.
    @classmethod
    def shareTag(cls, tagId: str, onwerId: str, otherId: str):
        tag = cls.getTag(tagId)
        if not tag:
            return None
        owner: User = Query(User, db.session).filter_by(id=onwerId).first()
        other: User = Query(User, db.session).filter_by(id=otherId).first()
        if not owner or not other:
            return None
        
        existingShare = Query(TagSharedUsers, db.session).filter_by(tagId=tag.id, userId=owner.id, sharedWithId=other.id).first()
        if existingShare:
            return existingShare
        tagShared = TagSharedUsers()
        tagShared.tagId = tag.id
        tagShared.userId = owner.id
        tagShared.sharedWithId = other.id
        tagShared.shareDate = datetime.now(timezone.utc)
        tag.updated = datetime.now(timezone.utc)
        try:
            db.session.add(tagShared)
            db.session.commit()
        except Exception as e:
            db.session.commit()
            return None
        return tagShared
    
    @classmethod
    def unShareTag(cls, tagId: str, ownerId: str, otherId: str):
        tag = cls.getTag(tagId)
        if not tag:
            return None
        owner = Query(User, db.session).filter_by(id=ownerId).first()
        other = Query(User, db.session).filter_by(id=otherId).first()
        if not owner or not other:
            return None
        sharedTag = Query(TagSharedUsers, db.session).filter_by(tagId=tag.id, userId=owner.id, sharedWithId=other.id).first()
        if not sharedTag:
            return None
        try:
            db.session.delete(sharedTag)
            db.session.commit()
        except Exception as e:
            db.session.commit()
            return None
        return tag
        
    
    @classmethod
    def getNotesInCampaign(cls, campaignId: str):
        notesWithinCamp = cls.query.filterBy(campaignId=campaignId).all()
        return notesWithinCamp
    
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
    def shareNoteDirectory(cls, ownerId: int, userIds: list[int], directory: str) -> list[Note]:
        directory = cls.normalizeDirectory(directory)
        users: list[User] = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return False
        
        for user in users:
            shared_directory =(
                Query(NoteSharedDirectories, db.session)
                .filter_by(userId=ownerId, sharedWithId=user.id, directory=directory)
                .first()
            )
            if not shared_directory:
                shared_directory = NoteSharedDirectories()
                shared_directory.userId = ownerId
                shared_directory.sharedWithId = user.id
                shared_directory.directory = directory
                shared_directory.shareDate = datetime.now(timezone.utc)
                db.session.add(shared_directory)
        db.session.commit()
        return True
    
    @classmethod
    def unShareNoteDirectory(cls, ownerId: int, userIds: list[int], directory: str):
        directory = cls.normalizeDirectory(directory)
        users: list[User] = Query(User, db.session).filter(User.id.in_(userIds)).all()
        if not users or len(users) == 0:
            return False
        
        for user in users:
            shared_directory = (
                Query(NoteSharedDirectories, db.session)
                .filter_by(userId=ownerId, sharedWithId=user.id, directory=directory)
                .first()
            )
            if not shared_directory:
                return False
            db.session.delete(shared_directory)
        db.session.commit()
        return True
    
    @classmethod
    def shareNoteToCampaign(cls, campaignId: str, noteId: str):
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
    
    @classmethod
    def unShareNoteFromCampaign(cls, noteId: str):
        note = cls.get(noteId)
        if not note:
            return None
        note.campaign = None
        note.updated = datetime.now(timezone.utc)
        db.session.commit()
        return note
    
    @classmethod
    def normalizeDirectory(cls, directory: str):
        directory = directory.strip()
        
        while directory.endswith('/'):
            directory = directory[:-1]
        return directory
    
    @classmethod
    def isSubDirectory(cls, parent: str, chid: str):
        parent = cls.normalizeDirectory(parent)
        child = cls.normalizeDirectory(child)
        
        if child == parent:
            return True
        return child.startswith(f"{parent}/")
    
    @classmethod
    def getParentDirectoryOf(cls, directory: str) -> str:
        directory = cls.normalizeDirectory(directory)
        if directory == '':
            return ''
        if "/" not in directory:
            return directory
        return directory.rsplit("/", 1)[0]
    
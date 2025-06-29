from datetime import datetime, timezone
from typing import List
from api.model.campaign import Campaign, CampaignCharacters, CampaignUsers
from api.model.character import Character
from api.model.user import User
from extensions import db
from sqlalchemy.orm import Query


class CampaignService:
    query = Query(Campaign, db.session)
    campaignUsersQuery = Query(CampaignUsers, db.session)
    campaignCharactersQuery = Query(CampaignCharacters, db.session)

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
    def addUserToCampaign(cls, campaignId: str, userId: User):
        for u in userId:
            if cls.campaignUsersQuery.filter_by(campaignId=campaignId, userId=u.id).first() is not None:
                return False
            campaignUser = CampaignUsers(campaignId=campaignId, userId=u.id, active=True)
            db.session.add(campaignUser)
            db.session.commit()
        return True
    
    @classmethod
    def addCharacterToCampaign(cls, campaignId: str, characterId: str):
        if Query(Character, db.session).filter_by(id=characterId).first() is None:
            return False
        if cls.campaignCharactersQuery.filter_by(campaignId=campaignId, characterId=characterId).first() is not None:
            return False
        campaignCharacter = CampaignCharacters(campaignId=campaignId, characterId=characterId, active=True)
        db.session.add(campaignCharacter)
        db.session.commit()
        return campaignCharacter

    @classmethod
    def create(cls, campaign: Campaign):
        campaign.active = True
        date_created = datetime.now(timezone.utc)
        campaign.created = date_created
        campaign.updated = date_created

        db.session.add(campaign)
        db.session.commit()
        return campaign

    @classmethod
    def updateCampaign(cls, id: str, campaign: Campaign):
        dbCampaign: Campaign = cls.query.filter_by(id=id).first()
        dbCampaign.name = (
            campaign.name if campaign.name is not None else dbCampaign.name
        )
        dbCampaign.description = (
            campaign.description if campaign.description is not None else dbCampaign.description
        )
        dbCampaign.active = (
            campaign.active if campaign.active is not None else dbCampaign.active
        )
        dbCampaign.updated = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def delete(cls, id: str):
        campaign: Campaign = cls.query.filter_by(id=id).first()

        if campaign is None:
            return False
        campaign.active = False
        db.session.commit()
        return True

    @classmethod
    def getCharactersByCampaignID(cls, id: str):
        results = (
            db.session.query(User)
            .join(CampaignCharacters, CampaignCharacters.userId == User.id)
            .filter(CampaignCharacters.campaignId == id, CampaignCharacters.active == True)
            .all()
        )
        return results

    @classmethod
    def getUsersByCampaignId(cls, id: str) -> List[User]:
        results = (
            db.session.query(User)
            .join(CampaignUsers, CampaignUsers.userId == User.id)
            .filter(CampaignUsers.campaignId == id, CampaignUsers.active == True)
            .all()
        )
        return results

    @classmethod
    def updateCampaignCharacters(cls, id: str, characters: list[Character]):
        campaign: Campaign = cls.query.filter_by(id=id).first()
        if campaign is None:
            return False
        campaign.characters = characters
        db.session.commit()
        return True
    
    @classmethod
    def getCampaignsByUserId(cls, userId: str):
        results = (
            db.session.query(Campaign)
            .join(CampaignUsers, CampaignUsers.campaignId == Campaign.id)
            .filter(CampaignUsers.userId == userId, CampaignUsers.active == True)
            .all()
        )
        return results
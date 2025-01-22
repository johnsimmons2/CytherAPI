from sqlalchemy.orm import Query
from api.model.character import Inventory, SharedInventory
from api.model.items import Items
from api.model.itemtypeenums import ItemBaseType, ItemCondition, ItemMaterial, ItemProperty, ItemRarity, ItemWeight
from api.service.dbservice import UserService
from api.service.repo.characterservice import CharacterService
from extensions import db
import api.service.jwthelper as jwth


class ItemsService:
    query = Query(Items, db.session)
    inventoryQuery = Query(Inventory, db.session)
    sharedInventoryQuery = Query(SharedInventory, db.session)
    
    @classmethod
    def translateType(cls, itemType: int):
        if int(itemType) < 0:
            raise ValueError("Invalid itemType: must be a positive integer.")
        itemType = int(itemType)
        strType = str(itemType)[::-1]
        baseType = int(strType[0]) if itemType >= 0 else 0
        rarity = int(strType[1]) if itemType >= 10 else 0
        weight = int(strType[2]) if itemType >= 100 else 0
        prop = int(strType[3]) if itemType >= 1_000 else 0
        stackable = int(strType[4]) <= 0 if itemType >= 10_000 else True
        condition = int(strType[5]) if itemType >= 100_000 else 0
        material = int(strType[6]) if itemType >= 1_000_000 else 0
        
        def _get_enum_display(enum_class, value):
            for member in enum_class:
                if member.value[0] == value:
                    return member.value[1]
            return "ERROR"
        
        baseTypeName = _get_enum_display(ItemBaseType, baseType)
        rarityName = _get_enum_display(ItemRarity, rarity)
        weightName = _get_enum_display(ItemWeight, weight)
        propName = _get_enum_display(ItemProperty, prop)
        conditionName = _get_enum_display(ItemCondition, condition)
        materialName = _get_enum_display(ItemMaterial, material)
        
        return {
            "baseType": baseTypeName,
            "rarity": rarityName,
            "weight": weightName,
            "property": propName,
            "stackable": stackable,
            "condition": conditionName,
            "material": materialName,
            "itemType": itemType,
        }
    
    @classmethod
    def getItemTranslated(cls, item: Items, shared: bool = False, admin: bool = False):
        return {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'type': cls.translateType(item.type),
            "shared": shared,
            "master": admin
        }
    
    @classmethod
    def getAll(cls):
        result = []        
        admin = jwth.has_role_level(0)
        currentUsername = jwth.get_username()
        
        items_with_relations = (
            cls.query
                .outerjoin(SharedInventory, SharedInventory.inventoryId == Items.id)
                .outerjoin(Inventory, Inventory.itemId == Items.id)
                .add_columns(
                    Inventory.characterId.label("characterId"),
                    SharedInventory.userId.label("sharedUserId"),
                )
                .all()
        )
        
        for item, characterId, sharedUserId in items_with_relations:
            ownedByUser = CharacterService.getOwnerUsernameFor(characterId) == currentUsername
            shared = sharedUserId == UserService.getUserIdFor(currentUsername)
            fromAdmin = admin and not ownedByUser and not shared
            
            result.append(cls.getItemTranslated(item, shared, fromAdmin))
        
        return result

    @classmethod
    def deleteInventoryItem(cls, inventory: Inventory):
        db.session.delete(inventory)
        db.session.commit()

    @classmethod
    def getInventoryItem(cls, id: str):
        item: Inventory = cls.inventoryQuery.filter_by(id=id).first()
        if item is None:
            return None
        return cls.get(item.itemId)
    
    @classmethod
    def getInventory(cls, id: str):
        return cls.inventoryQuery.filter_by(id=id).first()
    
    @classmethod
    def getCharacterInventory(cls, id: str):
        return cls.inventoryQuery.filter_by(characterId=id).all()

    @classmethod
    def get(cls, id: str):
        item = cls.query.filter_by(id=id).first()
        
        admin = False
        shared = False
        
        itemShared = cls.sharedInventoryQuery.filter_by(userId=UserService.getUserIdFor(jwth.get_username())).first()
        if itemShared is not None:
            shared = True
        else:
            if jwth.has_role_level(0):
                admin = True
        return cls.getItemTranslated(item, shared, admin)
    
    @classmethod
    def createItem(cls, name: str, description: str, itemType: int):
        foundItem = cls.query.filter(db.func.lower(Items.name) == name.lower()).filter(Items.type == itemType).first()
        if foundItem is not None:
            return foundItem, False
        
        item = Items()
        item.name = name
        item.description = description
        item.type = itemType
        db.session.add(item)
        db.session.commit()
        return item, True
    
    @classmethod
    def delete(cls, item: Items):
        db.session.delete(item)
        db.session.commit()
        
    # Return all the items in the database that a user has visibility to.
    @classmethod
    def getAllForUser(cls, charId: str):
        result = []        
        admin = jwth.has_role_level(0)
        currentUsername = jwth.get_username()
        
        items_with_relations = (
            cls.query
                .outerjoin(SharedInventory, SharedInventory.inventoryId == Items.id)
                .outerjoin(Inventory, Inventory.itemId == Items.id)
                .add_columns(
                    Inventory.characterId.label("characterId"),
                    SharedInventory.userId.label("sharedUserId"),
                )
                .all()
        )
        
        for item, characterId, sharedUserId in items_with_relations:
            ownedByUser = charId == characterId
            shared = sharedUserId == UserService.getUserIdFor(currentUsername)
            fromAdmin = admin and not ownedByUser and not shared
            
            if ownedByUser or shared or fromAdmin:
                result.append(cls.getItemTranslated(item, shared, fromAdmin))
        
        return result
    
    @classmethod
    def shareInventoryItem(cls, inventoryId: str, userId):
        inv: Inventory = cls.inventoryQuery.filter_by(id=inventoryId).first()
        if inv is None:
            return False
        
        shared = SharedInventory()
        shared.inventoryId = inventoryId
        shared.userId = userId
        
        inv.shared_with.append(shared)
        
        db.session.add(shared)
        db.session.commit()
        return True
    
    @classmethod
    def update(cls, item: Items):
        db.session.merge(item)
        db.session.commit()
        return item
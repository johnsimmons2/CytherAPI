from flask import Blueprint, request

from api.controller.controller import OK, BadRequest, Conflict, NotFound, Posted
from api.decorator.auth.authdecorators import isAdmin, isAuthorized
from api.loghandler.logger import Logger
from api.model.character import Character, Inventory
from api.model.item import Item
from api.service.repo.characterservice import CharacterService
from api.service.repo.itemservice import ItemsService


items = Blueprint('items', __name__)

@items.route("/items", methods = ['GET'])
@isAdmin
def getAll():
    curitems = ItemsService.getAll()
    if len(curitems) > 0:
        return OK(curitems)
    else:
        return NotFound("No items could be found in the database.")
    
@items.route("/items", methods = ['POST'])
@isAdmin
def createItem():
    requestJson = request.get_json()
    if requestJson is None:
        return BadRequest('No JSON was provided for the item.')
    
    if 'name' not in requestJson:
        return BadRequest('No name was provided for the item.')
    
    if 'description' not in requestJson:
        return BadRequest('No description was provided for the item.')
    
    itemType = 0
    if 'type' in requestJson:
        itemType = int(requestJson['type'])
        
    item, is_new = ItemsService.createItem(requestJson['name'], requestJson['description'], itemType)
    if item is not None:
        if is_new:
            return Posted(item)
        else:
            return Conflict(item)
    return BadRequest('Item could not be created.')

@items.route("/inventory/<itemId>/characters/<charId>", methods = ['POST'])
@isAdmin
def addItemToCharacter(itemId: str, charId: str):
    item: Item = ItemsService.get(itemId)
    character: Character = CharacterService.get(charId)
    quantity = request.args.get('quantity') or 1
    totalQuantity = int(quantity)
    
    if item is None:
        return NotFound("Item not found.")
    if character is None:
        return NotFound("Character not found.")
    
    characterInventory: list[Inventory] = ItemsService.getCharacterInventory(charId)
    if characterInventory is None or len(characterInventory) == 0:
        return NotFound("Character not found.")
    
    matchedInvItem = None
    for invItem in characterInventory:
        if invItem.itemId == int(itemId):
            totalQuantity = invItem.quantity + int(quantity)
            matchedInvItem = invItem
            break
    
    # We can remove items by adding negative quantity.
    if totalQuantity < 0 and matchedInvItem is not None:
        Logger.debug(f"Removing {quantity} of item {itemId} from character {charId} due to negative quantity.")
        ItemsService.deleteInventoryItem(matchedInvItem)
    
    # Create new Inventory item and add to the character
    charInventoryItem = Inventory()
    charInventoryItem.itemId = int(itemId)
    charInventoryItem.characterId = int(charId)
    charInventoryItem.quantity = totalQuantity
    # ItemsService.addItemToCharacter(item, character)
    return OK("Item added to character.")

@items.route("/items/<itemId>", methods = ['DELETE'])
@isAdmin
def deleteItem(itemId: str):
    item = ItemsService.get(itemId)
    if item is not None:
        ItemsService.delete(item)
        return OK("Item deleted.")
    return NotFound("Item not found.")

@items.route("/inventory/<inventoryId>", methods = ['GET'])
@isAuthorized
def getInventoryItem(inventoryId: str):
    items = ItemsService.getAllForUser(inventoryId)
    if len(items) > 0:
        return OK(items)
    return NotFound("No items could be found for the user.")

@items.route("/inventory/user/<userId>", methods = ['GET'])
@isAuthorized
def getItemsForUser(userId: str):
    curitems = ItemsService.getAllForUser(userId)
    if len(curitems) > 0:
        return OK(curitems)
    return NotFound("No items could be found for the user.")

@items.route("/inventory/<inventoryId>/share", methods = ['POST'])
@isAuthorized
def shareInventoryItem(inventoryId: str):
    item = ItemsService.getInventoryItem(inventoryId)
    inv = ItemsService.getInventory(inventoryId)
    if item is None or inv is None:
        return NotFound("Item not found.")
    
    requestJson = request.get_json()
    if requestJson is None:
        return BadRequest("No JSON was provided for the share.")
    
    if 'userIds' not in requestJson:
        return BadRequest("No user IDs were provided for the share.")
    
    for userId in requestJson['userIds']:
        try:
            ItemsService.shareInventoryItem(inventoryId, userId)
        except:
            Logger.error(f"Failed to share item {inventoryId} with user {userId}.")
    return OK("Inventory Item shared.")

@items.route("/items/<id>", methods = ['PATCH'])
@isAdmin
def updateItem(id: str):
    item: Item = ItemsService.get(id)
    if item is None:
        return NotFound("Item not found.")
    
    requestJson = request.get_json()
    if requestJson is None:
        return BadRequest("No JSON was provided for the update.")
    
    itemDto = Item()
    if 'name' in requestJson:
        itemDto.name = requestJson['name']
    if 'description' in requestJson:
        itemDto.description = requestJson['description']
    if 'type' in requestJson:
        itemDto.type = int(requestJson['type'])
    
    itemDto.id = int(id)
    
    newItem = ItemsService.update(itemDto)
    if newItem is not None:
        return OK(newItem)
    return BadRequest("Item could not be updated.")
    
@items.route("/items/type/<type>", methods = ['GET'])
@isAuthorized
def translateType(type: str):
    translated = ItemsService.translateType(type)
    return OK(translated)
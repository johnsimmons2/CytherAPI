# wstypes.py
import json
from enum import Enum


class WSType(Enum):
    WS = 'websocket'
    ACCEPT = 'websocket.accept'
    SEND = 'websocket.send'
    RECEIVE = 'websocket.receive'
    CONNECT = 'websocket.connect'
    DISCONNECT = 'websocket.disconnect'
    ERROR = 'websocket.error'

class WSAction(Enum):
    JOIN = 'join'           # Join a room
    LEAVE = 'leave'         # Leave a room
    CREATE = 'create'       # Create a room
    DELETE = 'delete'       # Delete a room
    INFO = 'info'           # No action, subtle information display
    LIST = 'list'
    LIST_PLAYERS = 'list_players'
    START = 'start'
    ROOM_UPDATE = 'room_update'
    PASS = 'pass'           # Pass turn
    NOTIFY = 'notify'       # Create pop up notification
    BROADCAST = 'broadcast' # Create pop up notification for all users
    STATUS = 'status'
    HEALTH = 'health'
    
    ERROR = 'error'         # Produce error message / log
    UNKNOWN = 'unknown'     # fail-through

class WSDamage:
    def __init__(self, owner, target, delta, commander=False):
        self.owner = owner
        self.target = target
        self.delta = delta
        self.commander = commander
    
    def __repr__(self):
        return f"{self.__dict__}"

class WSMessage:
    def __init__(self, action: WSAction, data):
        self.action = action
        self.data = data
    
class WSRoom:
    def __init__(self, owner, name, lock_to_turn = False, max_hp = 40):
        self.owner = owner
        self.name = name
        # Cannot join a started match unless you have joined in the past (auto)
        self.started = False
        # If True, only active player may change values on board
        self.lock_to_turn_owner = lock_to_turn
        self.max_hp = max_hp
        
        self.room_id = 0
        self.players: list[WSRoomOccupant] = []
        # Admin / owner sets this when hitting "start"
        self.turn = 0
        self.turn_index = 0
        
    def remove_player(self, user_id):
        for i,p in enumerate(self.players):
            if user_id == p.player.user_id:
                self.players.pop(i)
    
    def player_ids(self):
        ids = []
        for p in self.players:
            ids.append(p.player.user_id)
        return ids

class WSRoomOccupant:
    def __init__(self, player: "WSPlayer"):
        self.player = player
        self.online = False

class WSUser:
    def __init__(self, user_id, player: "WSPlayer", send: callable):
        self.user_id = user_id
        self.player = player
        self.send = send

class WSPlayer:
    def __init__(self, user, name, user_id, commander=None, max_hp=40):
        self.name = name
        self.commander = commander
        self.max_health = max_hp
        self.user_id = user_id
        
        self.health = max_hp
        self.connected = False
        self.active_turn = False
        self.room_id = None
        self.owned_room = None
        self.commander_damage = dict()
        
        self._user = user
    
    def __repr__(self):
        return f"'{self.name}' [{self.user_id}] ({self.health}/{self.max_health})"
    
    def ping(self, success: bool):
        if success:
            self.connected = True
        else:
            self.connected = False
            
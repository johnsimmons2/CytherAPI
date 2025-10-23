# wstypes.py
from dataclasses import dataclass, field
import json
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class WSType(Enum):
    WS = 'websocket'
    ACCEPT = 'websocket.accept'
    SEND = 'websocket.send'
    RECEIVE = 'websocket.receive'
    DISCONNECT = 'websocket.disconnect'

class WSAction(Enum):
    UNKNOWN = 'UNKNOWN'
    LIST_ROOMS = 'LIST_ROOMS'
    JOIN_ROOM = 'JOIN_ROOM'
    LEAVE_ROOM = 'LEAVE_ROOM'
    CREATE_ROOM = 'CREATE_ROOM'
    CLOSE_ROOM = 'CLOSE_ROOM'
    MESSAGE = 'MESSAGE'
    BROADCAST = 'BROADCAST'
    TURN_NEXT = 'TURN_NEXT'
    TURN_SET = 'TURN_SET'
    HEALTH = 'HEALTH'
    UPDATE_ROOM = 'UPDATE_ROOM'
    UPDATE_USER = 'UPDATE_USER'
    DISCONNECT = 'DISCONNECT'

@dataclass(frozen=True)
class WSMessage:
    action: WSAction
    data: Dict[str, Any]
    
    def to_json(self) -> str:
        return json.dumps({"action": self.action.value, "data": self.data})

@dataclass
class WSRoom:
    room_id: str
    name: str
    owner_id: int
    players: List["WSRoomOccupant"] = field(default_factory=list)
    turn_index: int = 0
    actual_turn_number: int = 0
    started: bool = False

    def has_player(self, user_id: int) -> bool:
        return any(o.player.user_id == user_id for o in self.players)

    def add_player(self, p: "WSPlayer", is_owner: bool = False) -> None:
        if not self.has_player(p.user_id):
            self.players.append(WSRoomOccupant(player=p, is_owner=is_owner))
            p.room_id = self.room_id

    def remove_player(self, user_id: int) -> None:
        self.players = [o for o in self.players if o.player.user_id != user_id]

    def current_turn_user_id(self) -> Optional[int]:
        if not self.players:
            return None
        idx = self.turn_index % len(self.players)
        return self.players[idx].player.user_id

    def next_turn(self) -> Optional[int]:
        if not self.players:
            return None
        self.turn_index = (self.turn_index + 1) % len(self.players)
        return self.current_turn_user_id()

    def set_turn_to(self, user_id: int) -> Optional[int]:
        for i, o in enumerate(self.players):
            if o.player.user_id == user_id:
                self.turn_index = i
                return user_id
        return None
    
    def to_public(self) -> Dict[str, Any]:
        return {
            "room_id": self.room_id,
            "name": self.name,
            "owner_id": self.owner_id,
            "turn_index": self.turn_index,
            "turn_user_id": self.current_turn_user_id(),
            "actual_turn": self.actual_turn_number,
            "players": [o.to_public() for o in self.players],
            "started": self.started
        }
    
@dataclass(frozen=True)
class WSDamage:
    owner: int
    target: int
    delta: int
    commander: bool = False

@dataclass
class WSRoomOccupant:
    player: "WSPlayer"
    is_owner: bool = False
    turn_index: int = 0

    def to_public(self) -> Dict[str, Any]:
        return {
            "player": self.player.to_public(),
            "is_owner": self.is_owner,
            "turn_index": self.turn_index
        }

@dataclass
class WSUser:
    user_id: int
    player: "WSPlayer"
    send: Callable[[Dict[str, Any]], Any]

@dataclass
class WSPlayer:
    _user: Any = None
    name: str = 'N/A'
    user_id: int = -1

    health: int = 40
    max_health: int = 40
    commander_damage: Dict[int, int] = field(default_factory=dict)

    connected: bool = False
    room_id: Optional[str] = None

    image: str = ''
    color: str = '#000000'
    
    def apply_damage(self, owner: int, delta: int, commander: bool = False):
        self.health += delta

        if commander and delta < 0:
            self.commander_damage[owner] = self.commander_damage.get(owner, 0) + (-delta)

    def to_public(self) -> Dict[str, Any]:
        return {
            "id": self.user_id,
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "commander_damage": dict(self.commander_damage),
            "room_id": self.room_id,
            "connected": self.connected,
            "image": self.image,
            "color": self.color
        }

    def __repr__(self):
        return f"'{self.name}' [{self.user_id}] ({self.health}/{self.max_health})"
    
    def ping(self, success: bool):
        if success:
            self.connected = True
        else:
            self.connected = False
            
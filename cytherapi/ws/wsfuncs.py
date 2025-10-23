# cytherapi/ws/wsfuncs.py (only key parts shown)
import json
from typing import Any, Dict, List, Optional
from . import wsstate as state
from .wstypes import (
    WSAction, WSMessage, WSType, WSRoom, WSUser, WSDamage, WSPlayer
)

def _ws_default_json(o):
    from .wstypes import json_default
    return json_default(o)

def to_payload(message: WSMessage, typ: WSType) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"type": typ.value}
    payload["text"] = json.dumps({"action": message.action.value, "data": message.data}, default=_ws_default_json)
    return payload

def error_message(msg: str) -> Dict[str, Any]:
    return {
        "type": WSType.SEND.value,
        "text": json.dumps({"type": "error", "message": msg})
    }

def list_rooms() -> Dict[str, Any]:
    rooms_public = [r.to_public() for r in state.ROOMS.values()]
    online_room = 0
    for r in state.ROOMS.values():
        online_room += sum([1 if c.player.connected else 0 for c in r.players])
    return {
        "type": WSType.SEND.value,
        "text": json.dumps({"action": WSAction.LIST_ROOMS.value, "rooms": rooms_public, "in_room": online_room, "online": len(state.ACTIVE.values())})
    }

async def _send_json(ws_user: WSUser, obj: Dict[str, Any]) -> None:
    await ws_user.send({"type": WSType.SEND.value, "text": json.dumps(obj)})

async def broadcast(obj: Dict[str, Any], recipients: List[WSUser]) -> None:
    dead: List[WSUser] = []
    for s in recipients:
        try:
            await _send_json(s, obj)
        except Exception:
            dead.append(s)
    if dead:
        # prune dead connections
        for d in dead:
            bucket = state.ACTIVE.get(d.user_id, [])
            if d in bucket:
                bucket.remove(d)
            if not bucket:
                state.ACTIVE.pop(d.user_id, None)

# --- Message routing ----------------------------------------------------------
async def route_message(scope, message: WSMessage):
    print(f"I just got the message: {message.action}-> {message.data}")

    action = message.action
    if action == WSAction.LIST_ROOMS:
        await scope["cyther.send"](list_rooms())

    elif action == WSAction.CREATE_ROOM:
        await create_room(scope, message.data.get("name") or "Room")

    elif action == WSAction.JOIN_ROOM:
        await join_room(scope, message.data.get("room_id"))
    
    elif action == WSAction.UPDATE_ROOM:
        await update_rooms_for_all()

    elif action == WSAction.LEAVE_ROOM:
        await leave_room(scope, message.data.get("room_id"))

    elif action == WSAction.CLOSE_ROOM:
        await close_room(scope, message.data.get("room_id"))

    elif action == WSAction.HEALTH:
        await apply_health(scope, message.data)

    elif action == WSAction.UPDATE_USER:
        await update_user(scope, message.data)

    elif action == WSAction.TURN_NEXT:
        await turn_next(scope, message.data.get("room_id"))

    elif action == WSAction.TURN_SET:
        await turn_set(scope, message.data.get("room_id"), message.data.get("user_id"))

    elif action == WSAction.DISCONNECT:
        pass
    else:
        await scope["cyther.send"](error_message(f"Unknown action: {action.value}"))

async def update_user(scope, player_data):
    room_id = player_data.get('room_id')
    room = state.ROOMS.get(room_id)

    np = WSPlayer()
    buckets = state.ACTIVE.get(player_data.get('id'))
    for b in buckets:
        if b.user_id == player_data.get('id'):
            np._user = b.player._user
            np.name = b.player.name
            np.user_id = b.player.user_id
            np.health = player_data.get('health')
            np.max_health = player_data.get('max_health')
            np.commander_damage = player_data.get('commander_damage')
            np.room_id = player_data.get('room_id')
            np.connected = player_data.get('connected')
            np.image = player_data.get('image')
            np.color = player_data.get('color')

            b.player = np
            break

    if room:
        for occ in room.players:
            if occ.player.user_id == player_data.get('id'):
                occ.player = np
                break
        await update_rooms_for_all()


async def update_rooms_for_all(only_not_in_room=False):
    recepients = []
    for bucket in state.ACTIVE.values():
        if bucket:
            for user in bucket:
                if only_not_in_room and user.player.room_id:
                    continue
                recepients.append(user)
    
    for r in recepients:
        await r.send(list_rooms())

async def update_players_in_room(room_id: str) -> None:
    await update_rooms_for_all()
    # room = state.ROOMS.get(room_id)
    # if not room:
    #     return
    # payload = {"action": WSAction.LIST_ROOMS.value, "rooms": room.to_public()}
    
    # # gather all sessions of people in the room
    # sessions: List[WSUser] = []
    # for occ in room.players:
    #     sessions.extend(state.connections(occ.player.user_id))
    # await broadcast(payload, sessions)

async def create_room(scope, name: str):
    player: WSPlayer = scope["cyther.player"]
    room_id = f"room-{player.user_id}"
    room = WSRoom(room_id=room_id, name=name, owner_id=player.user_id)
    room.add_player(player, is_owner=True)
    state.add_room(room)
    await update_rooms_for_all()
    await scope["cyther.send"]({"type": WSType.SEND.value, "text": json.dumps({"type":"room_created","room":room.to_public()})})

async def join_room(scope, room_id: Optional[str]):
    if not room_id or room_id not in state.ROOMS:
        await scope["cyther.send"](error_message("No such room"))
        return
    room = state.ROOMS[room_id]
    player: WSPlayer = scope["cyther.player"]
    if not room.has_player(player.user_id):
        room.add_player(player)
    await update_players_in_room(room_id)
    await update_rooms_for_all(True)

async def leave_room(scope, room_id: Optional[str]):
    player: WSPlayer = scope["cyther.player"]
    if not room_id:
        room_id = player.room_id
    if not room_id or room_id not in state.ROOMS:
        return
    room = state.ROOMS[room_id]
    room.remove_player(player.user_id)
    player.room_id = None

    # If owner leaves, decide policy (close room, transfer, etc.). For now, close if empty.
    if not room.players:
        state.remove_room(room_id)
    else:
        if room.owner == player.user_id:
            room.owner = room.players[0].player.user_id
            room.set_turn_to(room.owner)
    await update_players_in_room(room_id)
    await update_rooms_for_all(True)

async def close_room(scope, room_id: Optional[str]):
    if not room_id or room_id not in state.ROOMS:
        return
    state.remove_room(room_id)
    await scope["cyther.send"]({"type": WSType.SEND.value, "text": json.dumps({"type":"room_closed","room_id":room_id})})
    await update_rooms_for_all()

async def apply_health(scope, data: Dict[str, Any]):
    """data: { owner: int, deltas: [{target, delta, commander}] }"""
    owner = data.get("owner")
    deltas = data.get("deltas") or []
    sessions = state.connections(owner)

    if not sessions:
        return
    owner_player = sessions[0].player
    room_id = owner_player.room_id

    if not room_id:
        return
    room = state.ROOMS.get(room_id)
    if not room:
        return

    valid = {o.player.user_id for o in room.players}
    for d in deltas:
        tgt = d.get("target")
        if tgt not in valid:
            continue
        delta = int(d.get("delta", 0))
        cmd = bool(d.get("commander", False))
        for occ in room.players:
            if occ.player.user_id == tgt:
                print('applied damage')
                occ.player.apply_damage(owner, delta, commander=cmd)
                break
    await update_players_in_room(room_id)

async def turn_next(scope, room_id: Optional[str]):
    if not room_id:
        player: WSPlayer = scope["cyther.player"]
        room_id = player.room_id
    if not room_id or room_id not in state.ROOMS:
        return
    room = state.ROOMS[room_id]
    room.next_turn()
    await update_players_in_room(room_id)

async def turn_set(scope, room_id: Optional[str], user_id: Optional[int]):
    if not room_id or room_id not in state.ROOMS or user_id is None:
        return
    room = state.ROOMS[room_id]
    if room.set_turn_to(int(user_id)) is not None:
        await update_players_in_room(room_id)

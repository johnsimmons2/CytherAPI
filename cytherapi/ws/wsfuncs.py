# wsfuncs.py
import json
from enum import Enum
from .wstypes import WSAction, WSDamage, WSMessage, WSPlayer, WSRoom, WSRoomOccupant, WSType
from . import wsstate as state


async def disconnect(scope, manual = True):
    user = scope['cyther.user']
    player: WSPlayer = scope['cyther.player']
    try:
        pinger = scope['cyther.pinger']
        pinger.cancel()
    except:
        pass
    
    try:
        if player.room_id:
            room: WSRoom = state.ROOMS.get(player.room_id, None)
            if room:
                if manual:
                    if room.owner == player.user_id:
                        # close room
                        await close_room(scope, room.room_id)
                    else:
                        await leave_room(scope, room.room_id)
                else:
                    # If we did not try to quit on purpose, update our status.
                    await update_room(scope, room.room_id)
        
    except:
        pass
    state.ACTIVE.pop(getattr(user, "pk", None), None)

async def route_message(scope, message: WSMessage):
    player: WSPlayer = scope['cyther.player']
    send = scope['cyther.send']
    if message.action == WSAction.LIST:
        await send(list_rooms(scope))
    elif message.action == WSAction.LIST_PLAYERS:
        room_id = message.data
        await send(list_in_room(scope, room_id))
    elif message.action == WSAction.CREATE:
        rdata = message.data
        
        # If a user is already an owner, they cannot make another room.
        if player.room_id or player.owned_room:
            await send(error_message(scope, "Already in a room!"))
            return
        
        room = WSRoom(player.user_id, rdata['name'], rdata['lock_turns'], rdata['max_hp'])
        await create_room(scope, room)
    elif message.action == WSAction.DELETE:
        room_id = message.data
        if player.owned_room == room_id:
            await close_room(scope, room_id)
    elif message.action == WSAction.LEAVE:
        room_id = message.data
        await leave_room(scope, room_id)
    elif message.action == WSAction.JOIN:
        room_to_join = message.data
        await join_room(scope, room_to_join)
    elif message.action == WSAction.HEALTH:
        damage_data = message.data.get("deltas", None)
        damages: list[WSDamage] = []
        owner_pk = message.data.get("owner")
        
        sessions = state.ACTIVE.get(owner_pk, None)
        
        for s in sessions:
            owner: WSPlayer = s.player
            if owner is None:
                return
            owner_room = owner.room_id
            owner_id = owner.user_id
            for d in damage_data:
                room: WSRoom = state.ROOMS.get(owner_room)
                if not room or d['target'] not in [o.player.user_id for o in room.players]:
                    print("Can't target a player not in the current room!")
                    continue
                damages.append(WSDamage(owner_pk, d["target"], d["delta"], d.get("commander", False)))
            
            continue
    
        # process the damages
        for d in damages:
            sessions = state.ACTIVE.get(d.target)
            for occupant in room.players:
                if occupant.player.user_id == d.target:
                    p = occupant.player
                    p.health += d.delta
                    if d.commander and d.delta < 0:
                        prev = p.commander_damage.get(d.owner, 0)
                        p.commander_damage[d.owner] = prev + (-d.delta)
            
        await update_players_in_room(scope, owner_room)
    elif message.action == WSAction.START:
        '''
        Input looks like: 
            data: [first player's user_id, 2nd player's user_id, etc...]
        '''
        order: list[int] = list(message.data or [])
        room_id = player.room_id
        room: WSRoom = state.ROOMS.get(room_id)
        if not room:
            return await send(error_message(scope, "No room to start."))

        # Validate: every id in order must be in the room; allow subsets/ordering
        room_uids = [o.player.user_id for o in room.players]
        if not order or any(uid not in room_uids for uid in order):
            return await send(error_message(scope, "Turn order invalid."))

        room.turn_order = order
        room.turn_index = 0
        room.started = True

        # Set active_turn on players
        active_uid = order[0]
        for o in room.players:
            o.player.active_turn = (o.player.user_id == active_uid)

        state.ROOMS[room_id] = room
        await update_room(scope, room_id) 
    elif message.action == WSAction.STATUS:
        data = {
            "player": player
        }
        await send(to_payload(scope, WSMessage(WSAction.INFO, data), WSType.SEND))
    elif message.action == WSAction.PASS:
        room_id = player.room_id
        room: WSRoom = state.ROOMS.get(room_id)
        if not room or not getattr(room, "started", False):
            return await send(error_message(scope, "No active match."))

        order = getattr(room, "turn_order", None)
        if not order:
            return await send(error_message(scope, "Turn order not set."))

        current_uid = order[getattr(room, "turn_index", 0)]
        if player.user_id != current_uid and player.user_id != room.owner:
            return await send(error_message(scope, "Not your turn."))

        room.turn_index = (getattr(room, "turn_index", 0) + 1) % len(order)
        active_uid = order[room.turn_index]

        for o in room.players:
            o.player.active_turn = (o.player.user_id == active_uid)

        state.ROOMS[room_id] = room
        await update_room(scope, room_id)

async def close_room(scope, room_id):
    room: WSRoom = state.ROOMS.get(room_id, None)
    send = scope['cyther.send']
    
    if not room:
        return error_message(scope, "No room found to close.")
    
    for p in room.players:
        p.player.room_id = None
        p.player.owned_room = None
        p.player.health = p.player.max_health
        p.player.commander_damage = {}
        
        if p.player.room_id == room_id:
            p.player.room_id = None
        if p.player.owned_room == room_id:
            p.player.owned_room = None
        if p.player.user_id == scope['cyther.user_id']:
            scope['cyther.player'] = p.player
    
    room.players = []
    await update_room(scope, room_id)
    
    try:
        state.ROOMS.pop(room_id)
        await broadcast(scope, payload=list_rooms(scope))
    except:
        pass
    
    await send(to_payload(scope, WSMessage(WSAction.DELETE, room_id), WSType.SEND))

async def update_players_in_room(scope, room_id):
    '''
    Updates the room for players in the room
    '''
    room: WSRoom = state.ROOMS.get(room_id, None)
    updated_totals: list[WSRoomOccupant] = []
    subs = []
    for p in room.players:
        op = state.ACTIVE.get(p.player.user_id, None)
        if op == None:
            p.online = False
        else:
            p.online = True
            for ps in op:
                subs.append(ps.send)
                ps.player = p.player
                
        updated_totals.append(p)
    
    for sub in subs:
        await sub(to_payload(scope, WSMessage(WSAction.LIST_PLAYERS, updated_totals), WSType.SEND))

async def update_room(scope, room_id):
    '''
    Updates the room for ALL connected users
    '''
    room: WSRoom = state.ROOMS.get(room_id, None)
    if not room:
        return error_message(scope, "No room found to update.")
    
    await broadcast(scope, room, WSAction.ROOM_UPDATE)
        
async def broadcast(scope, msg_data=None, msg_action: WSAction=None, payload=None):
    if msg_action is None and payload is None:
        raise AssertionError("broadcast requires msg_action or payload")

    dead = []
    for uid, sessions in list(state.ACTIVE.items()):
        for ps in list(sessions):  # ps is WSUser
            try:
                pl = payload or to_payload(scope, WSMessage(msg_action, msg_data), WSType.SEND)
                await ps.send(pl)
            except Exception:
                dead.append((uid, ps))
    for uid, ps in dead:
        try:
            state.ACTIVE[uid].remove(ps)
        except ValueError:
            pass
        if not state.ACTIVE[uid]:
            state.ACTIVE.pop(uid, None)
    
async def create_room(scope, room: WSRoom):
    player: WSPlayer = scope['cyther.player']
    id = state.CURRENT_ID
    
    room_occupant = WSRoomOccupant(player)
    room_occupant.online = True

    room.room_id = id
    room.players = [room_occupant]
    room.owner = player.user_id
    player.room_id = room.room_id
    player.owned_room = room.room_id
    scope['cyther.player'] = player
    state.ROOMS[id] = room
    state.CURRENT_ID += 1
    
    await broadcast(scope, payload=list_rooms(scope))

async def leave_room(scope, room_id):
    player: WSPlayer = scope['cyther.player']
    room: WSRoom = state.ROOMS.get(room_id, None)
    send = scope['cyther.send']
    
    if not room or player.room_id != room_id:
        return await send(error_message(scope, "Cannot leave room player is not in."))
        
    try:
        room.remove_player(player.user_id)
        player.room_id = None
        scope['cyther.player'] = player
    except:
        print("User was not connected or joined.")
    
    state.ROOMS[room.room_id] = room
    await update_room(scope, room.room_id)
    
    await send(to_payload(scope, WSMessage(WSAction.NOTIFY, f"Left {room.name}."), WSType.SEND))
        
async def join_room(scope, room_id):
    player: WSPlayer = scope['cyther.player']
    room: WSRoom = state.ROOMS.get(room_id, None)
    send = scope['cyther.send']
    
    if not room or player.room_id or player.owned_room is not None:
        return await send(error_message(scope, "Cannot join room player is already in or does not exist."))
    
    if room.started:
        return await send(error_message(scope, "Cannot join room with a match in progress."))
    
    try: 
        room.players.append(WSRoomOccupant(player))
        player.room_id = room_id
        scope['cyther.player'] = player
        state.ROOMS[room_id] = room
        await update_room(scope, room_id)
    except:
        import traceback
        traceback.print_exc()
    
    await send(to_payload(scope, WSMessage(WSAction.NOTIFY, f"Joined {room.name}."), WSType.SEND))

def list_in_room(scope, room_id):
    '''
    List all the global rooms in current state
    '''
    room: WSRoom = state.ROOMS.get(room_id, None)
    if not room:
        return to_payload(scope, WSMessage(WSAction.ERROR, 'Room was not found'), WSType.SEND)
    
    players = room.players
    for p in players:
        up = state.ACTIVE.get(p.player.user_id, None)
        if up is None:
            p.online = False
        else:
            p.online = True
    
    return to_payload(scope, WSMessage(WSAction.LIST_PLAYERS, players), WSType.SEND)

def list_rooms(scope):
    rooms = []
    if len(state.ROOMS.items()) > 0:
        for _,room in state.ROOMS.items():
            rooms.append(room)
    return to_payload(scope, WSMessage(WSAction.LIST, rooms), WSType.SEND)

def to_payload(scope, message: WSMessage, type: WSType):
    payload = {
        "type": type.value
    }
    
    if message.action == WSAction.BROADCAST:
        payload['from'] = scope['cyther.user']
    
    payload['text'] = json.dumps(message, default=_ws_default_json)
    return payload

def error_message(scope, error_txt):
    return to_payload(scope, WSMessage(WSAction.ERROR, error_txt), WSType.SEND)

def _ws_default_json(o):
    if isinstance(o, Enum):
        return o.value
    elif isinstance(o, WSMessage):
        return {
            "action": o.action.value,
            "data": o.data
        }
    elif isinstance(o, (str, int, float)):
        return o
    if hasattr(o, "__dict__"):
        return {k: v for k, v in o.__dict__.items() if not k.startswith("_")}
    raise TypeError(f"Could not serialize: {type(o)}")
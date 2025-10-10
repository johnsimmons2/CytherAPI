# wsstate.py
from cytherapi.ws.wstypes import WSUser


ACTIVE: dict[str, list[WSUser]] = dict() # everyone listening
ROOMS = dict() # currently online, roomId -> array of players
IN_ROOMS = [] # anyone who joins a room is duplicated here, you cannot enter more than one room.
CURRENT_ID = 1

PING_INTERVAL = 25

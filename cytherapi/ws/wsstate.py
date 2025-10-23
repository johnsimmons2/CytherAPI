# cytherapi/ws/wsstate.py
from __future__ import annotations

import asyncio
from typing import Dict, List, Optional
from .wstypes import WSRoom, WSUser

# Ping timing
PING_INTERVAL = 25

ACTIVE: Dict[int, List[WSUser]] = {}     # user_id -> open connections
ROOMS: Dict[str, WSRoom] = {}            # room_id -> room

_ROOM_LOCKS: Dict[str, asyncio.Lock] = {}

def room_lock(room_id: str) -> asyncio.Lock:
    lk = _ROOM_LOCKS.get(room_id)
    if lk is None:
        lk = asyncio.Lock()
        _ROOM_LOCKS[room_id] = lk
    return lk

def get_room(room_id: str) -> Optional[WSRoom]:
    return ROOMS.get(room_id)

def add_room(room: WSRoom) -> None:
    ROOMS[room.room_id] = room

def remove_room(room_id: str) -> None:
    ROOMS.pop(room_id, None)

def connections(user_id: int) -> List[WSUser]:
    return ACTIVE.get(user_id, [])

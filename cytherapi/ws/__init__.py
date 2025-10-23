# __init__.py
import json, asyncio
import logging
from enum import Enum
from http.cookies import SimpleCookie
from importlib import import_module
from typing import Dict, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .wsfuncs import error_message, list_rooms, route_message, to_payload
from .wstypes import WSAction, WSMessage, WSPlayer, WSType, WSUser
from . import wsstate as state

log = logging.getLogger(__name__)

ACTION_BY_VALUE: Dict[str, WSAction] = {a.value: a for a in WSAction}

def _get_cookies(scope):
    headers = dict(scope.get("headers", []))
    raw = headers.get(b"cookie", b"").decode()
    c = SimpleCookie()
    c.load(raw)
    
    return {k: v.value for k, v in c.items()}

def _load_session(session_key: str):
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore(session_key)

    store.load()
    return store

async def _load_user_from_session(session_key: str):
    try:
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore(session_key)

        # Run the blocking load in a thread and capture the dict it returns.
        data = await sync_to_async(store.load, thread_sensitive=True)()
        # Optional: prime Django's cache so future 'store.get' doesn't re-load:
        # setattr(store, "_session_cache", data)

        uid = data.get("_auth_user_id")
        if not uid:
            return None

        User = get_user_model()
        # Wrap ORM call too
        user = await sync_to_async(
            lambda: User.objects.filter(pk=uid).first(),
            thread_sensitive=True
        )()
        return user

    except Exception:
        log.exception("Failed to load user from session")
        return None

def _parse_message(text: str) -> Optional[WSMessage]:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    action = ACTION_BY_VALUE.get(obj.get("action",""), WSAction.UNKNOWN)
    data = obj.get("data", {})
    if not isinstance(data, dict):
        data = {"value": data}
    return WSMessage(action, data)

async def get_message(message_text, scope, send):
    msg = _parse_message(message_text)
    if msg is None:
        await send(error_message("bad json"))
    return msg

async def _pinger(send):
    try:
        while True:
            await asyncio.sleep(state.PING_INTERVAL)
            await send({"type": WSType.SEND.value,
                        "text": json.dumps({"type": "ping"})})
    except asyncio.CancelledError:
        return
    except Exception:
        log.exception("Ping task error")

async def websocket_handler(scope, receive, send):
    assert scope["type"] == WSType.WS.value

    # ---- Authenticate via Django session cookie ----
    cookies = _get_cookies(scope)
    session_key = cookies.get(settings.SESSION_COOKIE_NAME)
    user = await _load_user_from_session(session_key) if session_key else None

    # --- DEBUG ---
    SKIP_USER_FOR_DEBUG = False
    # -------------

    if SKIP_USER_FOR_DEBUG:
        import random
        class Test:
            pass
        user = Test()
        fake_uid = random.randrange(1, 100)
        setattr(user, "pk", fake_uid)
        setattr(user, "username", f"user-{fake_uid}")
    else:
        if not user:
            print('Denied access to websocket to anonymous user!')
            await send({"type": "websocket.close", "code": 4401})  # 4401 Unauthorized
            return

    player = WSPlayer(user, user.username, getattr(user, "pk", None))
    player.connected = True
    for r in state.ROOMS.values():
        if r.has_player(player.user_id):
            player.room_id = r.room_id

    ws_user = WSUser(player.user_id, player, send)
    scope["cyther.user"] = user
    scope["cyther.user_id"] = player.user_id
    scope["cyther.player"] = player
    scope["cyther.send"] = send
    scope["cyther.ws_user"] = ws_user
    
    # ---- Accept and proceed ----
    await send({"type": WSType.ACCEPT.value})
    
    # TODO: Allow for multiple devices under one user connection.
    state.ACTIVE.setdefault(player.user_id, []).append(ws_user)

    list_room_message = list_rooms()
    print(f'player {scope["cyther.player"]} connected.')
    print(f'Sending list of rooms: {list_room_message}')
    print(f"Users: {[ k for k in state.ACTIVE.keys() ]}")
    print('--------')
    await send(list_room_message)
    
    ping_task = None
    try:
        ping_task = asyncio.create_task(_pinger(send))
        scope['cyther.pinger'] = ping_task

        while True:
            event = await receive()
            etype = event["type"]
            if etype == WSType.RECEIVE.value:
                message_str = event.get("text") or "{}"
                message: WSMessage = await get_message(message_str, scope, send)
                if message is None:
                    continue
                
                await route_message(scope, message)
            elif etype == WSType.DISCONNECT.value:
                break
    finally:
        uid = getattr(user, 'pk', None)
        w = scope.get('cyther.ws_user')
        bucket = state.ACTIVE.get(uid)

        if bucket:
            try: 
                bucket.remove(w)
            except ValueError:
                pass
            if not bucket:
                state.ACTIVE.pop(uid, None)
        task = scope.get('cyther.pinger')
        if task:
            task.cancel()
            try:
                await task
            except:
                pass
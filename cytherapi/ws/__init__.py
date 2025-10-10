# __init__.py
import json, asyncio
from enum import Enum
from http.cookies import SimpleCookie
from importlib import import_module
from django.conf import settings
from django.contrib.auth import get_user_model
from .wsfuncs import error_message, list_rooms, route_message, to_payload
from .wstypes import WSAction, WSMessage, WSPlayer, WSType, WSUser
from . import wsstate as state


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

async def get_message(message_text, scope, send):
    print("Received:")
    print(f"Event: {message_text}")
    print("--------")
    
    try:
        json_message = json.loads(message_text)
        action_text = json_message.get('action', '')
        action = WSAction.UNKNOWN
        for a in WSAction:
            if a.value == action_text:
                action = a
        
        return WSMessage(action, json_message.get('data', {}))
    except Exception:
        import traceback
        traceback.print_exc()
        await send(error_message(scope, 'bad json'))
        return None

async def websocket_handler(scope, receive, send):
    assert scope["type"] == WSType.WS.value

    # ---- Authenticate via Django session cookie ----
    cookies = _get_cookies(scope)
    session_key = cookies.get(settings.SESSION_COOKIE_NAME, None)  # default 'sessionid'
    user = None
    if session_key:
        try:
            session = _load_session(session_key)
            user_id = session.get("_auth_user_id")
            if user_id:
                User = get_user_model()
                user = User.objects.filter(pk=user_id).first()
        except Exception:
            user = None  # treat as anonymous on any failure

    # if not user:
    #     print('Denied access to websocket to anonymous user!')
    #     await send({"type": "websocket.close", "code": 4401})  # 4401 Unauthorized
    #     return
    import random
    class Test:
        pass
    user = Test()
    setattr(user, "pk", random.randrange(1, 100))

    player = WSPlayer(user, 'asdasd', getattr(user, "pk", None))
    player.connected = True
    scope["cyther.user"] = user
    scope["cyther.user_id"] = player.user_id
    scope["cyther.player"] = player
    scope["cyther.send"] = send
    
    # ---- Accept and proceed ----
    await send({
        "type": WSType.ACCEPT.value
    })
    
    ws_user = WSUser(player.user_id, player, send)
    
    # TODO: Allow for multiple devices under one user connection.
    uid = player.user_id
    if uid in state.ACTIVE:
        state.ACTIVE[uid].append(ws_user)
    else:
        state.ACTIVE[player.user_id] = [ws_user]
    scope["cyther.ws_user"] = ws_user
    list_room_message = list_rooms(scope)
    print(f'player {scope["cyther.player"]} connected.')
    print(f'Sending list of rooms: {list_room_message}')
    print(f"Users: {[ k for k in state.ACTIVE.keys() ]}")
    print('--------')
    await send(list_room_message)
    
    try:
        ping_task = asyncio.create_task(_pinger(send))
        scope['cyther.pinger'] = ping_task
        while True:
            event = await receive()
            if event["type"] == WSType.RECEIVE.value:
                message_str = event.get("text") or "{}"
                message: WSMessage = await get_message(message_str, scope, send)
                if message == None:
                    continue
                
                await route_message(scope, message)
            elif event["type"] == WSType.DISCONNECT.value:
                break
    finally:
        uid = getattr(user, 'pk', None)
        w = scope.get('cyther.ws_user')
        if uid in state.ACTIVE:
            try:
                state.ACTIVE[uid].remove(w)
            except ValueError:
                pass
            if not state.ACTIVE[uid]:
                state.ACTIVE.pop(uid, None)
        ping_task.cancel()
        

async def _pinger(send):
    while True:
        await asyncio.sleep(state.PING_INTERVAL)
        await send({
            "type": WSType.SEND.value, 
            "text": json.dumps({
                "type": "ping"
            })
        })
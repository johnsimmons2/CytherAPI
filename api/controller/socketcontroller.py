
from enum import Enum
from flask import Blueprint, request
from flask_socketio import emit, join_room, leave_room, disconnect
from api.controller.controller import OK, NotFound, ServerError
from api.decorator.auth.authdecorators import isAuthorized
from api.loghandler.logger import Logger
from api.service.dbservice import UserService
from api.service.jwthelper import decode_token, get_access_token
from api.service.repo.skillservice import SkillService
from extensions import socketio


wsocket = Blueprint('ws', __name__)

connected_users = {}

class SocketEvent(Enum):
    CONNECT = 'connect'
    DISCONNECT = 'disconnect'
    MESSAGE = 'message'
    JOIN = 'join'
    LEAVE = 'leave'

class SocketMessage:
    def __init__(self, event: SocketEvent, data: dict, message: str | None  = None):
        self.event = event
        self.data = data
        self.message = message or f'{event.name} event received'

def remove_connected_user():
    try:
        session_id = request.sid
        for u in connected_users.keys():
            if connected_users[u]['session_id'] == session_id:
                Logger.debug(f'Client removed from connected users list: {session_id} from user {u}.')
                user = connected_users[u]
                del connected_users[u]
                break
    except:
        Logger.error('Failed to disconnect client from websocket. Was the client already disconnected?')

def force_disconnect():
    remove_connected_user()
    disconnect()

@wsocket.route("/ws", methods = ['GET'])
def index():
    return OK("Websocket is working")

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    
    Logger.debug(f'Attempt to connect to websocket: {session_id}')
    token = decode_token(get_access_token())
    if not token:
        Logger.debug('No token provided')
        force_disconnect()
        return
    Logger.debug(f'Token was validated: {session_id}')
    # Check if the user is already connected by this token
    username = token["username"]
    
    if username in connected_users.keys():
        Logger.debug(f'User {username} is already connected')
        force_disconnect()
        return
    
    connected_users[username] = {
        'user': UserService.getByUsername(username),
        'session_id': session_id
    }
    
    Logger.debug(f"Client connected to websocket in room {username}")
    emit('response', {'message': 'Connected to WebSocket'})
    
@socketio.on('disconnect')
def handle_disconnect():
    Logger.debug(f"Received a disconnect request from {request.sid}")
    remove_connected_user()
    emit('disconnect', {'message': 'Disconnected from websocket'})

@socketio.on('message')
def handle_message(data):
    Logger.debug(f"Message received: {data}")
    emit('response', {'message': 'Message received!'}, broadcast=True)
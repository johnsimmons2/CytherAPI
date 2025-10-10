"""
ASGI config for cytherapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from .ws import websocket_handler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cytherapi.settings')
asgi_app = get_asgi_application()

async def application(scope, receive, send):
    print(scope["type"])
    print(scope.get("path","").startswith("/ws/"))
    if scope["type"] == "websocket" and scope.get("path","").startswith("/ws/"):
        await websocket_handler(scope, receive, send)
        return
    await asgi_app(scope, receive, send)

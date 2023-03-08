"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path
from events.consumers import EchoConsumer
import events.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    # WebSocket handler
    # "websocket": AuthMiddlewareStack(
    #     URLRouter([
    #         re_path(r"^ws/echo/$", EchoConsumer.as_asgi()),
    #     ])
    # ),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(events.routing.websocket_urlpatterns)
        )
    ),
})

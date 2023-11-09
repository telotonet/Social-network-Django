from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chatting.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import layout.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueprint_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            layout.routing.websocket_urlpatterns
        )
    ),
})

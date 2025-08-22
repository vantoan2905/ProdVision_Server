"""
ASGI config for app_django project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_django.settings")

django_asgi_app = get_asgi_application()


from app_django.jwt_middleware.jwt_middleware import JwtAuthMiddleware
import provision.urls.camera_routing as routing  

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JwtAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

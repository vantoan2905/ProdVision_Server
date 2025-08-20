from django.urls import re_path
from provision.views.camera_views import CameraWebSocketView

websocket_urlpatterns = [
    re_path(r"ws/camera/(?P<camera_id>\d+)/$", CameraWebSocketView.as_asgi()),
]

from django.urls import re_path
from provision.views.camera_views import CameraWebSocketView

websocket_urlpatterns = [
    # TODO: Authenticate client
    # TODO: Stream video frames from server to client
    # TODO: Write turn on/off funtionality for detection object in file path_to_file="view/camera_views.py"
    re_path(r"ws/camera/(?P<camera_id>\d+)/$", CameraWebSocketView.as_asgi()),
]

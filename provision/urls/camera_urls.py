from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from provision.views.camera_views import CameraRequestView, GetAllCamerasView,  ObjectDetectorView
from provision.views.camera_views import CameraRequestView, LoadAllCamerasView
urlpatterns = [
    path('load_all_camera/', LoadAllCamerasView.as_view(), name='load_all_camera'),

    path('request_camera/', CameraRequestView.as_view(), name='request_camera'),
    # path('detect_object/', ObjectDetectorView.as_view(), name='detect_object'),
]

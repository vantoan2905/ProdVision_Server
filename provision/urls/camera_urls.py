from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from provision.views.camera_views import CameraRefreshView

urlpatterns = [
    path('load_all_camera/', CameraRefreshView.as_view(), name='load_all_camera'),
    path('load_pretrained_model/', CameraRefreshView.as_view(), name='load_pretrained_model'),
    path('detect_object/', CameraRefreshView.as_view(), name='detect_object'),

]

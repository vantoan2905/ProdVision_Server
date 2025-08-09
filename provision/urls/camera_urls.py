from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from provision.views.camera_views import CameraManagerView

urlpatterns = [
    path('load_all_camera/', CameraManagerView.as_view(), name='load_all_camera'),
    path('load_pretrained_model/', CameraManagerView.as_view(), name='load_pretrained_model'),
    path('detect_object/', CameraManagerView.as_view(), name='detect_object'),

]

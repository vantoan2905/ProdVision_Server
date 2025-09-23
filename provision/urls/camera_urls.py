
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from provision.views.camera_views import CameraViewSet, CameraErrorViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')
router.register(r'camera_errors', CameraErrorViewSet, basename='camera_error')

urlpatterns = [
    path('', include(router.urls)),
]


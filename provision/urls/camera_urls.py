from django.urls import path
from provision.views.camera_views import (
    CameraRequestView,
    LoadAllCamerasView,
    CameraDetailView,
    CameraStartView,
    CameraStopView,
    CameraSnapshotView,
    CameraErrorsView,
    ErrorDetailView,
    ErrorAcknowledgeView,
    CapturedImagesView,
    ErrorStatisticsView,
)

urlpatterns = [
    path('cameras/', LoadAllCamerasView.as_view(), name='load_all_cameras'),
    path('cameras/<int:pk>/', CameraDetailView.as_view(), name='camera_detail'),
    path('cameras/<int:pk>/start/', CameraStartView.as_view(), name='camera_start'),
    path('cameras/<int:pk>/stop/', CameraStopView.as_view(), name='camera_stop'),
    path('cameras/<int:pk>/snapshot/', CameraSnapshotView.as_view(), name='camera_snapshot'),
    path('cameras/<int:pk>/errors/', CameraErrorsView.as_view(), name='camera_errors'),
    path('errors/<int:pk>/', ErrorDetailView.as_view(), name='error_detail'),
    path('errors/<int:pk>/acknowledge/', ErrorAcknowledgeView.as_view(), name='error_acknowledge'),
    path('cameras/<int:pk>/captured-images/', CapturedImagesView.as_view(), name='captured_images'),
    path('errors/statistics/', ErrorStatisticsView.as_view(), name='error_statistics'),

    path('request_camera/', CameraRequestView.as_view(), name='request_camera'),
]

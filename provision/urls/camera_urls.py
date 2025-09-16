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
    CreateCameraView
)

default_urls_camera = "camera_manager"
default_urls_error = "error_manager"
urlpatterns = [
    path(f"{default_urls_camera}/", LoadAllCamerasView.as_view(), name="load_all_cameras"),
    path(f"{default_urls_camera}/<int:pk>/", CameraDetailView.as_view(), name="camera_detail"),
    path(f"{default_urls_camera}/<int:pk>/start/", CameraStartView.as_view(), name="camera_start"),
    path(f"{default_urls_camera}/<int:pk>/stop/", CameraStopView.as_view(), name="camera_stop"),
    path(f"{default_urls_camera}/<int:pk>/snapshot/", CameraSnapshotView.as_view(), name="camera_snapshot"),
    path(f"{default_urls_camera}/<int:pk>/errors/", CameraErrorsView.as_view(), name="camera_errors"),
    path(f"{default_urls_camera}/<int:pk>/captured-images/", CapturedImagesView.as_view(), name="captured_images"),
    path(f"{default_urls_camera}/create_new_camera/", CreateCameraView.as_view(), name="create_new_camera"),

    path(f"{default_urls_error}/<int:pk>/", ErrorDetailView.as_view(), name="error_detail"),
    path(f"{default_urls_error}/<int:pk>/acknowledge/", ErrorAcknowledgeView.as_view(), name="error_acknowledge"),
    path(f"{default_urls_error}/statistics/", ErrorStatisticsView.as_view(), name="error_statistics"),

    path("request_camera/", CameraRequestView.as_view(), name="request_camera"),
]


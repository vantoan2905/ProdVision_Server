from django.shortcuts import get_object_or_404
from provision.models import Camera
import cv2


class CameraService:
    _connections = {}  # cache {camera_id: cv2.VideoCapture}

    @staticmethod
    def check_camera_permission(user, camera):
        return user.is_superuser or camera.owner == user

    @staticmethod
    def get_camera_by_id(camera_id):
        return get_object_or_404(Camera, camera_id=camera_id)

    @staticmethod
    def get_all_cameras(user_id):
        return Camera.objects.filter(owner__id=user_id).values_list("camera_id", flat=True)

    @staticmethod
    def add_new_camera(user_id, camera_name, camera_key, camera_info):
        return Camera.objects.create(
            owner_id=user_id,          
            camera_name=camera_name,
            camera_key=camera_key,
            camera_info=camera_info    
        )

    @staticmethod
    def update_camera(camera_id, camera_name=None, camera_key=None, camera_info=None):
        camera = CameraService.get_camera_by_id(camera_id)
        if camera_name:
            camera.camera_name = camera_name
        if camera_key:
            camera.camera_key = camera_key
        if camera_info:
            camera.camera_info = camera_info 
        camera.save()
        return camera

    @staticmethod
    def delete_camera(camera_id):
        qs = Camera.objects.filter(camera_id=camera_id)
        if qs.exists():
            qs.delete()
            return True
        return False

    @staticmethod
    def check_if_camera_exists(camera_id):
        return Camera.objects.filter(camera_id=camera_id).exists()

    @staticmethod
    def check_if_camera_active(camera_id):
        return True  # placeholder, implement real check

    @staticmethod
    def check_if_camera_connected(camera_id):
        return True  # placeholder, implement real check

    @staticmethod
    def connect_to_camera(camera_id, video_path=None):
        """
        Connect to a camera and return the connection object.

        Args:
            camera_id (int): ID of the camera to connect to.
            video_path (str, optional): Path to the video file to use as the camera stream. Defaults to None.

        Raises:
            ValueError: If the video source cannot be opened.

        Returns:
            cv2.VideoCapture: The connection object for the camera.
        """
        if camera_id in CameraService._connections:
            return CameraService._connections[camera_id]

        if video_path is None:
            video_path = f"media/videos/{camera_id}.mp4"

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video source for camera {camera_id}")

        CameraService._connections[camera_id] = cap
        return cap

    @staticmethod
    def release_camera(camera_id):
        cap = CameraService._connections.get(camera_id)
        if cap:
            cap.release()
            del CameraService._connections[camera_id]

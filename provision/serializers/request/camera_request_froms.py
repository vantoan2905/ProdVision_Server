from rest_framework import serializers

class CameraRequestFrom(serializers.Serializer):
    id_camera = serializers.IntegerField()
    key_camera = serializers.CharField(
        max_length=255
    )

class CreateCameraRequestFrom(serializers.Serializer):
    camera_name = serializers.CharField(
        max_length=255
    )
    camera_key = serializers.CharField(
        max_length=255
    )
    camera_info = serializers.CharField(
        max_length=255
    )
class UpdateCameraRequestFrom(serializers.Serializer):
    camera_id = serializers.IntegerField()
    camera_name = serializers.CharField(
        max_length=255
    )
    camera_key = serializers.CharField(
        max_length=255
    )
    camera_info = serializers.CharField(
        max_length=255
    )
class LoadAllCamerasRequestFrom(serializers.Serializer):
    id_user_id = serializers.IntegerField()



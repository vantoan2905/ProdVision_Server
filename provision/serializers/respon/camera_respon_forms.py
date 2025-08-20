# provision/serializers/user_serializers.py

from rest_framework import serializers

class CameraResponseFrom(serializers.Serializer):
    id_camera = serializers.IntegerField()
    key_camera = serializers.CharField()

    # Nếu muốn custom field từ hàm, phải dùng SerializerMethodField
    id_camera_info = serializers.SerializerMethodField()

    def get_id_camera_info(self, obj):
        # Ví dụ: xử lý custom
        return f"Camera-{obj['id_camera']}"

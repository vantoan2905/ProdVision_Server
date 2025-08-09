from django.db import models
from provision.models.user_models import User
from provision.models.camera_info import CameraInfo

class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    camera_name = models.CharField(max_length=255, null=True, blank=True)
    camera_key = models.CharField(max_length=255, null=True, blank=True)
    camera_info = models.ForeignKey(CameraInfo, on_delete=models.CASCADE, related_name="cameras")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cameras")

    def __str__(self):
        return self.camera_name or f"Camera {self.camera_id}"

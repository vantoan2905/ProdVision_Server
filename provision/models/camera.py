from django.db import models
from .status_type import CameraStatus, CameraType

class Camera(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    type = models.ForeignKey(CameraType, on_delete=models.SET_NULL, null=True, related_name='cameras')
    status = models.ForeignKey(CameraStatus, on_delete=models.SET_NULL, null=True, related_name='cameras')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

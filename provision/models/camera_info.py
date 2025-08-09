from django.db import models

class CameraInfo(models.Model):
    model_name = models.CharField(max_length=255, null=True, blank=True)
    resolution_max = models.CharField(max_length=50, null=True, blank=True)
    resolution_min = models.CharField(max_length=50, null=True, blank=True)
    fps_max = models.IntegerField(null=True, blank=True)
    fps_min = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.model_name or f"Camera {self.id}"

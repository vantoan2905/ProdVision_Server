from django.db import models

class MLModel(models.Model):
    # model name
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, blank=True, null=True)
    snapshot_url = models.URLField(blank=True, null=True)


class Error(models.Model):
    type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    position = models.JSONField(blank=True, null=True)
    acknowledged = models.BooleanField(default=False)

from django.db import models
from .status_type import ModelStatus, ModelType

class Model(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    type = models.ForeignKey(ModelType, on_delete=models.SET_NULL, null=True, related_name='models')
    status = models.ForeignKey(ModelStatus, on_delete=models.SET_NULL, null=True, related_name='models')
    accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name','version')

    def __str__(self):
        return f"{self.name} v{self.version}"

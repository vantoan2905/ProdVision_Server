 
from django.db import models
from .model_family import ModelFamily

class ModelAI(models.Model):
    family = models.ForeignKey(ModelFamily, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    framework = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.framework})"

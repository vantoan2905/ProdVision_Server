 
from django.db import models
from .model_ai import ModelAI

class ModelVersion(models.Model):
    model = models.ForeignKey(ModelAI, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=50)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('dev', 'Development'),
        ('prod', 'Production'),
        ('deprecated', 'Deprecated')
    ], default='dev')
    file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model.name} - {self.version}"

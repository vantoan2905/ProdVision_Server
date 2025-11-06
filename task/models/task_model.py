 
from django.db import models
from .task import Task
from ...vision.models.model_version import ModelVersion
from ...vision.models.dataset import Dataset

class TaskModel(models.Model):
    ACTION_CHOICES = [
        ('train', 'Train'),
        ('eval', 'Evaluate'),
        ('update', 'Update'),
        ('deploy', 'Deploy')
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    model_version = models.ForeignKey(ModelVersion, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    result_metric = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    log_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

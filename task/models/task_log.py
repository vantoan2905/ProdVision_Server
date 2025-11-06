 
from django.db import models
from .task import Task

class TaskLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Info'),
        ('WARN', 'Warning'),
        ('ERROR', 'Error'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='INFO')
    created_at = models.DateTimeField(auto_now_add=True)

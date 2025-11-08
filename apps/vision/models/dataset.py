 
from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    record_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

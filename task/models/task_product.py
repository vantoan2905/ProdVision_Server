 

from django.db import models
from .task import Task
from ...product.models.product import Product

class TaskProduct(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    usage_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('task', 'product')

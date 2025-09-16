from django.db import models
from .employee import Employee
from .product import Product
from .models_ai import Model

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    has_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TaskEmployee(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_employees')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    assigned_at = models.DateTimeField(auto_now_add=True)

class TaskProduct(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tasks')

class TaskModel(models.Model):
    ACTION_CHOICES = [
        ('train','Train'),
        ('eval','Eval'),
        ('update','Update')
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_models')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='task_models')
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

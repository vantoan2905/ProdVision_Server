  
from django.db import models
from .department import Department
from .role import Role

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

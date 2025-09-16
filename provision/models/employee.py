from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_code = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.employee_code})"

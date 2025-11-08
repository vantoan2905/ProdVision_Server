 
from django.db import models
from .task import Task
from ...employee.models.employee import Employee

class TaskEmployee(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_role = models.CharField(max_length=50, blank=True, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'employee')

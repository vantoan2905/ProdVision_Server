from django.db import models
from .camera import Camera
from .models_ai import Model
from .product import Product
from .status_type import ViewStatus, DefectType
from .task import Task
from .employee import Employee

class View(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='views')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='views')
    status = models.ForeignKey(ViewStatus, on_delete=models.SET_NULL, null=True, related_name='views')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Inspection(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='inspections')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inspections')
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, related_name='inspections')
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, related_name='inspections')
    view = models.ForeignKey(View, on_delete=models.SET_NULL, null=True, related_name='inspections')
    defect_detected = models.BooleanField(default=False)
    defect_type = models.ForeignKey(DefectType, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspections')
    confidence = models.FloatField(null=True, blank=True)
    image_path = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    inspected_at = models.DateTimeField(auto_now_add=True)

    def work_duration(self):
        """Trả về số giờ làm việc nếu employee tham gia"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds() / 3600
        return 0

    def __str__(self):
        return f"Inspection {self.id} - {self.product.name}"

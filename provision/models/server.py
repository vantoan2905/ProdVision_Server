from django.db import models
from .models_ai import Model
from .status_type import ServerStatus, DeploymentStatus

class Server(models.Model):
    ip_address = models.GenericIPAddressField()
    hostname = models.CharField(max_length=100)
    status = models.ForeignKey(ServerStatus, on_delete=models.SET_NULL, null=True, related_name='servers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

class ModelDeployment(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='deployments')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='deployments')
    deployed_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(DeploymentStatus, on_delete=models.SET_NULL, null=True, related_name='deployments')

    def __str__(self):
        return f"{self.model.name} on {self.server.hostname}"

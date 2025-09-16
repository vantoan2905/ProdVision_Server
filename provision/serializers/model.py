from rest_framework import serializers
from .models import MLModel, Error

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ["id", "name", "status", "snapshot_url"]


class CreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ["name", "status", "snapshot_url"]


class UpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ["status", "snapshot_url"]
        extra_kwargs = {
            "status": {"required": False},
            "snapshot_url": {"required": False},
        }


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = ["id", "type", "level", "position", "acknowledged"]

# files/serializers.py
from rest_framework import serializers
from .models import KnowledgeChunk, FileRecord
from django.contrib.auth.models import User


class ImageProcessingSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, help_text="Image file (JPEG, PNG, GIF)")


class HistorySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    query = serializers.CharField()
    response = serializers.CharField()
    timestamp = serializers.DateTimeField()
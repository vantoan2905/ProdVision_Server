# files/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class MessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100)


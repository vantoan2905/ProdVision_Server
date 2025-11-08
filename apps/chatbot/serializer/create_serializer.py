
from rest_framework import serializers


class CreateChatSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
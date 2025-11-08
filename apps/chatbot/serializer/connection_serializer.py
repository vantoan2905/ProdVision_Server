from rest_framework import serializers

class ConnectionSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
    question = serializers.CharField(required=True)
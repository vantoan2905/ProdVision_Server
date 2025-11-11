from rest_framework import serializers


class DeleteChatSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100, required=True)
    user_id = serializers.CharField(max_length=100, required=True)
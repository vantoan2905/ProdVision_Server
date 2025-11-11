from rest_framework import serializers


class ListChatSessionSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=True)
    limit = serializers.IntegerField(required=False)
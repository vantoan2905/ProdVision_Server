from rest_framework import status, serializers

class ChatbotSerializer(serializers.Serializer):
    message = serializers.CharField()
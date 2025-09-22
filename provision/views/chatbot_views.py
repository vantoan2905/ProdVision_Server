from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# WebSocket setup
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from provision.serializers.chatbot import ChatbotSerializer


class ChatbotSessionView(APIView):
    """
    REST API for creating a chatbot session / issuing JWT tokens.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class ChatbotChatView(APIView):
    """
    REST API endpoint to send a message into the chatbot channel.
    In practice, real-time messages will be handled by a WebSocket consumer.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChatbotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data.get("message")
        user = request.user.username

        # Send the message to the channel layer (chatbot group)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chatbot_group",
            {
                "type": "chat_message",  # event name that consumer listens for
                "message": message,
                "user": user,
            },
        )

        return Response(
            {"status": "sent", "message": message, "user": user},
            status=status.HTTP_200_OK,
        )

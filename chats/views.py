from django.shortcuts import render
from ollama import Client
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from chats.serializers import MessageSerializer
from django.http import StreamingHttpResponse
from datetime import datetime
from rest_framework.response import Response
from drf_yasg import openapi
from chats.models import ChatSession
from sentence_transformers import SentenceTransformer
from rest_framework import status
from chats.service import ChatService




import json
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from chats.service import ChatService
from chats.serializers import MessageSerializer
from chats.utils.image import tensor_to_base64

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from drf_yasg.utils import swagger_auto_schema
from chats.service import ChatService
from chats.serializers import MessageSerializer

class ChatMessageView(APIView):

    @swagger_auto_schema(
        operation_description="Chat SSE streaming with tool-based AI Agent",
        tags=["Chat"],
        request_body=MessageSerializer,
    )
    def post(self, request):
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "content is required"},
                status=400
            )

        chat_service = ChatService()

        def event_stream():
            try:
                for event in chat_service.stream_chat(content):
                    """
                    event schema (pipeline 2):
                    {
                        "type": "text",
                        "content": str
                    }
                    or
                    {
                        "type": "chart",
                        "chart_type": str,
                        "title": str,
                        "data": { labels: [...], values: [...], ... }
                    }
                    """

                    # ------------------------------
                    # TEXT STREAM
                    # ------------------------------
                    if event["type"] == "text":
                        payload = {
                            "type": "text",
                            "content": event["content"],
                        }
                        yield f"data: {json.dumps(payload)}\n\n"

                    # ------------------------------
                    # CHART (SEND JSON DATA)
                    # ------------------------------
                    elif event["type"] == "chart":
                        payload = {
                            "type": "chart",
                            "chart_type": event["chart_type"],
                            "title": event.get("title"),
                            "data": event.get("data"),  # JSON data for frontend rendering
                        }
                        yield f"data: {json.dumps(payload)}\n\n"


                yield "event: done\ndata: [DONE]\n\n"

            except Exception as e:
                yield f"event: error\ndata: {str(e)}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response




class ChatHistoryView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve chat history for a given session and user.",
        tags=["Chat"],
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_STRING),
        ],
        responses={200: MessageSerializer(many=True)}
    )
    def get(self, request):
        user_id = request.GET.get('user_id')
        chat_service = ChatService()
        history = chat_service.get_history_sessions(user_id)
        return Response(history, status=200)



class DeleteHistoryView(APIView):
    @swagger_auto_schema(
        operation_description="Delete all chat sessions and history for a user.",
        tags=["Chat"],
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="User ID",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: "All sessions deleted successfully",
            400: "Failed to delete sessions"
        }
    )
    def delete(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({"error": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)

        chat_service = ChatService()
        success = chat_service.delete_all_session(user_id)

        if success:
            return Response({"message": f"All sessions for user {user_id} deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to delete sessions"}, status=status.HTTP_400_BAD_REQUEST)


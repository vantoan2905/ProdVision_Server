import json
from django.http import StreamingHttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication

from chats.service.chat_service_port import ChatServicePort
from chats.service.provider import get_chat_service
from auth_app.lib.permissions import JWTOptional
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class ChatMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        body = json.loads(request.body.decode("utf-8"))
        content = body.get("content")
        if not content:
            return JsonResponse({"error": "content is required"}, status=400)

        chat_service: ChatServicePort = get_chat_service()

        def event_stream():
            for event in chat_service.stream_chat_sync(content):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

        return StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream"
        )


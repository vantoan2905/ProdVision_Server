import json
from django.http import StreamingHttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from chats.service.chat_service_port import ChatServicePort
from chats.service.provider import get_chat_service


@method_decorator(csrf_exempt, name="dispatch")
class ChatMessageView(View):

    async def post(self, request, *args, **kwargs):
        # print("RAW BODY:", request.body)

        try:
            body = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        content = body.get("content")
        if not content:
            return JsonResponse({"error": "content is required"}, status=400)

        # get interface
        chat_service: ChatServicePort = get_chat_service()

        async def event_stream():
            try:
                async for event in chat_service.stream_chat(content):
                    yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"

        return response


# django
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from apps.chatbot.servicies.llm_service import LLMService
import json

# serializer
from apps.chatbot.serializer.create_serializer import CreateChatSessionSerializer
from apps.chatbot.serializer.connection_serializer import ConnectionSerializer
from apps.chatbot.serializer.delete_session_serializer import DeleteChatSessionSerializer
from apps.chatbot.serializer.list_session_serializer import ListChatSessionSerializer
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

llm_service = LLMService(use_api=False, retriever=None)
# decorate swagger docstrings


@swagger_auto_schema(
    method='post',
    request_body=CreateChatSessionSerializer,
    responses={200: openapi.Response("Tạo session thành công")},
)
@api_view(["POST"])
def create_session(request):
    serializer = CreateChatSessionSerializer(data=request.data)
    if serializer.is_valid():
        session_id = serializer.validated_data["session_id"]
        llm_service.create_session(session_id)
        return Response({"message": f"Session {session_id} created successfully."})
    return Response(serializer.errors, status=400)





@api_view(["GET"])
def get_history(request, session_id):

    history = llm_service.get_history(session_id)
    return Response({"session_id": session_id, "history": history})




@swagger_auto_schema(
    method='post',
    request_body=ConnectionSerializer,
    responses={200: openapi.Response("Kết nối SSE thành công")},
)
@api_view(["POST"])
def chat_stream(request):
    question = request.data.get("question")
    # user_id = request.data.get("user_id")
    user_id = "test"
    session_id = request.data.get("session_id")
    

    collected_chunks = []

    def event_stream():
        try:
            docs = llm_service.retriever.invoke(question) if llm_service.retriever else []
            context = "\n".join([d.page_content for d in docs])
            chat_history = "\n".join(llm_service.get_history(session_id)[-10:])

            for chunk in llm_service.chain.stream({
                "question": question,
                "documents": context,
                "chat_history": chat_history,
            }):
                collected_chunks.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"

            answer = "".join(collected_chunks)

            llm_service.sessions[session_id].append(f"Q: {question}")
            llm_service.sessions[session_id].append(f"A: {answer}")

            llm_service.save_history(session_id, question, answer, user_id)

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")




@swagger_auto_schema(
    method='delete',
    request_body=DeleteChatSessionSerializer,
    responses={200: openapi.Response("Delete session successfully")},
)
@api_view(["DELETE"])
def delete_session(request):
    session_id = request.data.get("session_id")
    user_id = request.data.get("user_id")

    ok = llm_service.delete_session(session_id, user_id)
    if not ok:
        return Response({"message": "not found"}, status=404)

    return Response({"message": f"deleted session {session_id}"})


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'user_id',
            openapi.IN_QUERY,
            description='filter sessions by user_id',
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description='limit number of sessions returned',
            type=openapi.TYPE_INTEGER,
            required=False
        ),
    ],
    responses={200: openapi.Response("List sessions successfully")},
)
@api_view(["GET"])
def list_sessions(request):
    user_id = request.GET.get("user_id")
    limit = request.GET.get("limit")

    sessions = llm_service.list_sessions(user_id=user_id, limit=limit)
    print(sessions)
    return Response({"sessions": sessions})

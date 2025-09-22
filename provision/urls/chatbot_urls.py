from django.urls import path
from provision.views.chatbot_views import (
    ChatbotSessionView,
    ChatbotChatView,
)

app_name = "chatbot_management"

urlpatterns = [
    path("create_session/", ChatbotSessionView.as_view(), name="create_session"),
    path("chat/", ChatbotChatView.as_view(), name="chat"),
]

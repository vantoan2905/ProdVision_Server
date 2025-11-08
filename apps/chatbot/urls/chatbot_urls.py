from django.urls import path
from apps.chatbot.views import chatbot_views as views

urlpatterns = [
    path("session/create/", views.create_session, name="chatbot-create-session"),
    path("session/<str:session_id>/history/", views.get_history, name="chatbot-get-history"),
    path("session/<str:session_id>/stream/", views.chat_stream, name="chatbot-stream"),
]

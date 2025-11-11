from django.urls import path
from apps.chatbot.views import chatbot_views as views

urlpatterns = [
    # session
    path("session/create/", views.create_session, name="chatbot-create-session"),
    path("session/stream/", views.chat_stream, name="chatbot-stream"),
    path("session/delete/", views.delete_session, name="chatbot-delete-session"),
    path("session/<str:user_id>/<str:limit>/list/", views.list_sessions, name="chatbot-list-sessions"),
    # sse chat
    path("session/<str:session_id>/history/", views.get_history, name="chatbot-get-history"),
    

]

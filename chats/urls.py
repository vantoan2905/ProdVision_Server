from django.urls import path
from chats.views import (
    ChatMessageView,
    ChatHistoryView,
    DeleteHistoryView
)
urlpatterns = [
    path('send-message/', ChatMessageView.as_view(), name='send-message'),
    path('chat-history/', ChatHistoryView.as_view(), name='chat-history'),
    path('delete-chat-history/', DeleteHistoryView.as_view(), name='delete-chat-history'),
]
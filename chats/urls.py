from django.urls import path
from chats.views import (
    ChatMessageView,

)
urlpatterns = [
    path('send-message/', ChatMessageView.as_view(), name='send-message'),

]
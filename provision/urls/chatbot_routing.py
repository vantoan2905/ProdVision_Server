from django.urls import re_path
from provision.views.chatbot_consumer import ChatbotConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatbotConsumer.as_asgi()),
]

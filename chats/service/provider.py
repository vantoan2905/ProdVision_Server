from chats.service.chat_service_port import ChatServicePort
from chats.service.chat_service_impl import ChatServiceImpl

def get_chat_service() -> ChatServicePort:
    return ChatServiceImpl()

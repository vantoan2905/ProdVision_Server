from typing import Protocol, AsyncGenerator

class ChatServicePort(Protocol):
    async def stream_chat(self, content: str) -> AsyncGenerator[dict, None]:
        ...

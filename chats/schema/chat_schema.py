
from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessageInput:
    content: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None




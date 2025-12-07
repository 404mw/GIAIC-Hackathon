from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    conversation_history: Optional[List[str]] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

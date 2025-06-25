from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str
    tool_name: Optional[str] = None 
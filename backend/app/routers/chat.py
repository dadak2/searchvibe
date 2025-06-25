from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.agent import search_products, chat_sessions

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """채팅 엔드포인트 - Agent를 통한 상품 검색"""
    try:
        # Agent를 통한 상품 검색
        response_text, tool_name = await search_products(request.message, thread_id=request.thread_id)
        return ChatResponse(response=response_text, tool_name=tool_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류가 발생했습니다: {str(e)}")

@router.get("/history")
async def get_chat_history():
    """모든 thread_id별 멀티턴 대화 히스토리 반환 (개발/디버깅용)"""
    return chat_sessions 
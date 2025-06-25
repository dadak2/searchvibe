import os
from typing import Optional, Dict, List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

# thread_id별 대화 히스토리 (메모리 저장)
chat_sessions: Dict[str, List[dict]] = {}

# MCP 툴 비동기 로딩 (최초 1회)
_mcp_tools = None
async def get_mcp_tools():
    global _mcp_tools
    if _mcp_tools is not None:
        return _mcp_tools
    naver_url = os.getenv("NAVER_MCP_URL")
    exa_url = os.getenv("EXA_MCP_URL")
    client = MultiServerMCPClient({
        "naver_search_mcp": {
            "url": naver_url,
            "transport": "streamable_http",
        },
        "exa_search_mcp": {
            "url": exa_url,
            "transport": "streamable_http",
        },
    })
    _mcp_tools = await client.get_tools()
    return _mcp_tools


def create_agent(checkpointer=None, tools=None):
    """LangGraph React Agent를 생성합니다."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    system_prompt = """
    당신은 상품 최저가 검색 전문 어시스턴트입니다.
    사용자가 요청한 상품에 대해 판매 사이트가 반드시 리스트업 되도록 검색어를 수정하고 웹 검색을 통해 상품리스트를 찾으세요.
    한국어로 유용하고 정확한 상품 최저가 정보와 구매 링크를 제공해야 합니다.

    답변에는 반드시 아래 항목을 포함하세요:
    1. 상품명과 가격 정보
    2. 구매 가능한 쇼핑몰 또는 사이트 링크 (아래 예시 쇼핑몰을 참고하여 국내외 주요 쇼핑몰을 반드시 리스트업)
    - 쿠팡, 11번가, SSG, Naver쇼핑 등
    3. 각 쇼핑몰별로 상품명, 가격, 구매 링크를 표 형태로 정리, 최대 5개로 제한

    위 정보들을 포함하여 친절하고 상세하게 답변하세요.
    """
    agent = create_react_agent(
        llm,
        tools,
        prompt=system_prompt,
        checkpointer=checkpointer
    )
    return agent


async def search_products(query: Optional[str], thread_id: Optional[str] = None) -> Tuple[str, str]:
    """멀티턴 대화 지원: thread_id별로 대화 히스토리 관리, MCP 웹검색 툴 사용 (비동기)
    반환값: (assistant 응답, 실제 사용된 MCP 툴명)"""
    if not query or query.strip() == "":
        return ("검색어를 입력해주세요.", "-")
    thread_id = thread_id or "default"
    messages = chat_sessions.get(thread_id, [])
    messages.append({"role": "user", "content": query})
    try:
        checkpointer = InMemorySaver()
        tools = await get_mcp_tools()
        agent = create_agent(checkpointer=checkpointer, tools=tools)
        result = await agent.ainvoke({"messages": messages}, {"configurable": {"thread_id": thread_id}})
        tool_name = "알 수 없음"
        # MCP 툴 사용 정보 추출 (metadata 또는 messages에서 추정)
        if result and "metadata" in result and "tool" in result["metadata"]:
            tool_name = result["metadata"]["tool"]
        elif result and "messages" in result:
            for msg in result["messages"]:
                if type(msg).__name__ == "ToolMessage" and hasattr(msg, "name"):
                    tool_name = msg.name
        if result and "messages" in result and len(result["messages"]) > 0:
            last_message = result["messages"][-1]
            messages.append({"role": "assistant", "content": last_message.content})
            chat_sessions[thread_id] = messages
            return last_message.content, tool_name
        else:
            return "검색 결과를 가져올 수 없습니다.", tool_name
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}", "-" 
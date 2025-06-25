# 온라인 쇼핑 최저가 검색 챗봇 서비스 - searchvibe

## 서비스 소개
온라인 쇼핑 시 여러 쇼핑몰의 상품 가격을 자동으로 검색·비교하여 최저가 정보를 제공하는 AI 챗봇 웹서비스입니다. 사용자는 챗봇에 상품명을 입력하면, 실시간으로 다양한 쇼핑몰의 가격·할인·배송비·구매링크 등 종합 정보를 한 번에 확인할 수 있습니다.

## 주요 기능
- **실시간 최저가 검색**: 다양한 쇼핑몰의 상품 가격을 자동으로 수집·비교
- **대화형 챗봇 인터페이스**: 자연어로 상품명 입력, 결과 리스트 제공
- **할인/배송비/구매링크 안내**: 단순 가격뿐 아니라 부가 정보까지 종합 안내
- **스트리밍 응답**: 검색 진행상황 및 결과를 실시간으로 표시
- **에러 핸들링**: 검색 실패 시 안내 메시지 제공

## 기술 스택
### 백엔드
- **언어/프레임워크**: Python 3.11, FastAPI
- **AI/Agent**: LangGraph (Pre-built React Agent), Google Gemini LLM
- **웹검색**: LangChain DuckDuckGo Search Tool
- **테스트**: pytest
- **서버**: uvicorn (ASGI)

### 프론트엔드
- **언어/프레임워크**: Python 3.11, Streamlit
- **용도**: 챗봇 UI, 검색 결과 표시

## 폴더 구조
```
vibe_coding/
├── backend/           # FastAPI 백엔드
│   ├── app/           # 앱 모듈 (agent, models, routers 등)
│   ├── requirements.txt
│   ├── run.py         # 서버 실행 스크립트
│   └── tests/         # 백엔드 테스트 코드
├── frontend/          # Streamlit 프론트엔드
│   ├── app.py         # 챗봇 UI
│   └── requirements.txt
├── docs/              # 기획/UX 문서
├── .env.example       # 환경 변수 예시
└── README.md
```

## 실행 방법
### 1. 환경 변수 설정
- `backend/env.example` 파일 참고하여 `.env` 파일 생성 및 API 키 등 입력

### 2. 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 3. 프론트엔드 실행
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## API 예시
- POST `/chat/` : { "message": "아이폰 15" } → 최저가 검색 결과 반환

## 개발 목표 및 비전
- **시간 절약**: 수동 가격 비교 시간을 90% 단축
- **정보 통합**: 여러 쇼핑몰 정보를 한 곳에서 확인
- **실시간 대화**: 자연스러운 챗봇 인터페이스
- **TDD/클린아키텍처**: 테스트 우선, SOLID 원칙, 작은 단위의 함수/파일

## 참고 라이브러리
- [FastAPI 공식문서](https://fastapi.tiangolo.com/)
- [Streamlit 공식문서](https://docs.streamlit.io/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [DuckDuckGo Search Tool](https://github.com/deedy5/duckduckgo_search)

---
문의: [프로젝트 관리자에게 연락]

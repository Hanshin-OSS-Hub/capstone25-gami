# FastAPI 서버의 시작점
# 앱을 생성하고, 라우터를 등록하고, 서버 시작 시 필요한 초기 로딩 작업을 연결하는 역할만 맡음

from fastapi import FastAPI
from api.dialogue_router import router as dialogue_router
from api.session_router import router as session_router
from services.semantic_memory_service import load_semantic_memory
from services.neo4j_init_service import ensure_default_npc

app = FastAPI()

# 서버 시작 시 MongoDB에서 semantic memory를 최초 1회 로드
@app.on_event("startup")
def startup_event():
    load_semantic_memory()
    
    ensure_default_npc()

# 대화 관련 API 등록
app.include_router(dialogue_router)

# 세션 종료 API 등록
app.include_router(session_router)
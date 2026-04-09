# 대화 종료 시 메모리 상태를 Neo4j에 반영하는 API를 제공

from fastapi import APIRouter, HTTPException
from services.state_memory_service import flush_session_state
from services.session_state_service import get_all_session_states

router = APIRouter(prefix="/session", tags=["session"])

# 현재 FastAPI 메모리에 올라와 있는 세션 상태를 확인
@router.get("/states")
def read_session_states():
    return {"states": get_all_session_states()}

# 대화 종료 시 state memory를 Neo4j에 저장하고 세션을 정리
@router.post("/end")
def end_session(player_id: str, npc_id: str):
    try:
        saved_state = flush_session_state(player_id, npc_id)

        if saved_state is None:
            return {"message": "저장할 세션 상태가 없습니다."}

        return {
            "message": "세션 상태를 Neo4j에 저장했습니다.",
            "state": saved_state
        }

    except Exception as e:
        print("session end error:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
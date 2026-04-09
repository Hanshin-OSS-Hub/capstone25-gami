# Unity가 보내는 NPC 대화 요청을 받는 라우터
# 플레이어 발화를 받고, 내부적으로 dialogue_service를 호출한 뒤, 최종 응답을 Unity에 반환

from fastapi import APIRouter, HTTPException
from schemas.dialogue_schema import DialogueReq, DialogueRes
from services.dialogue_service import process_dialogue

router = APIRouter()

# 서버가 정상 실행 중인지 확인하는 테스트용 API
@router.get("/health")
def health():
    return {"ok": True}

# Unity의 메시지를 받아 NPC 응답을 생성해서 반환하는 API
@router.post("/dialogue", response_model=DialogueRes)
def dialogue(req: DialogueReq):
    try:
        npc_text = process_dialogue(
            npc_id=req.npc_id,
            player_id=req.player_id,
            user_text=req.user_text
        )

        return {"npc_text": npc_text}

    except Exception as e:
        print("dialogue error:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
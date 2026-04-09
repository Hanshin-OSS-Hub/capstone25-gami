# Unity ↔ FastAPI 대화 요청/응답 형식을 정의

from pydantic import BaseModel

# Unity -> FastAPI로 들어오는 대화 요청 형식
class DialogueReq(BaseModel):
    npc_id: str
    player_id: str
    user_text: str

# FastAPI -> Unity로 반환하는 대화 응답 형식
class DialogueRes(BaseModel):
    npc_text: str
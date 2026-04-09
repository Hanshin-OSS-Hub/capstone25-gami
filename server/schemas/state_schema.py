# NPC state memory 형식을 정의

from pydantic import BaseModel

class StateMemory(BaseModel):
    npc_id: str
    player_id: str
    affinity: int
    trust: int
    mood: int
    view_of_player: str
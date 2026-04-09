# Neo4j의 state memory를 FastAPI 메모리에 로드하고, 종료 시 다시 저장

import random
from core.neo4j import driver

from repositories.state_memory_repository import (
    load_state_memory_from_neo4j,
    save_state_memory_to_neo4j
)
from services.session_state_service import (
    get_session_state,
    set_session_state,
    remove_session_state
)


# 대화 시작 시 사용할 랜덤 mood(기분) 값 생성 (-5 ~ 5)
def generate_random_mood():
    return random.randint(-5, 5)


# 세션 상태가 없으면 Neo4j에서 읽어와 FastAPI 메모리에 올림
def ensure_session_state(player_id: str, npc_id: str):
    state = get_session_state(player_id, npc_id)

    if state is not None:
        return state

    state = load_state_memory_from_neo4j(player_id, npc_id)

    if state is None:
        return None

    state["mood"] = generate_random_mood()

    set_session_state(player_id, npc_id, state)

    return state


# 세션 상태를 메모리에서 수정
def update_session_state(player_id: str, npc_id: str, updates: dict):
    state = ensure_session_state(player_id, npc_id)

    for key, value in updates.items():
        state[key] = value

    set_session_state(player_id, npc_id, state)
    return state


# 대화가 끝날 때 메모리 상태를 Neo4j에 저장하고 세션에서 제거
def flush_session_state(player_id: str, npc_id: str):

    state = get_session_state(player_id, npc_id)

    if state is None:
        return None

    save_state_memory_to_neo4j(
        player_id=player_id,
        npc_id=npc_id,
        affinity=state["affinity"],
        trust=state["trust"],
        view_of_player=state["view_of_player"]
    )

    remove_session_state(player_id, npc_id)
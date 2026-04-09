# 현재 대화 세션 동안 FastAPI 메모리에 state memory를 저장

_session_state_cache = {}

# player_id:npc_id 조합으로 세션 키 제작
def build_session_key(player_id: str, npc_id: str) -> str:
    return f"{player_id}:{npc_id}"

# 세션 상태 저장
def set_session_state(player_id: str, npc_id: str, state: dict):
    session_key = build_session_key(player_id, npc_id)
    _session_state_cache[session_key] = state

# 세션 상태 읽기
def get_session_state(player_id: str, npc_id: str):
    session_key = build_session_key(player_id, npc_id)
    return _session_state_cache.get(session_key)

# 세션 상태 삭제
def remove_session_state(player_id: str, npc_id: str):
    session_key = build_session_key(player_id, npc_id)
    return _session_state_cache.pop(session_key, None)

# 현재 메모리에 올라와 있는 전체 세션 상태를 반환
def get_all_session_states():
    return _session_state_cache
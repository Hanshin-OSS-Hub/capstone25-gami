# 현재 대화 중인 NPC가 제3 NPC와의 관계 정보를 redis에 일정 대화 동안 유지하고 프롬프트용 텍스트로 변환하는 로직
import json
from core.redis import redis_client

# 대화중인 NPC-제 3NPC 관계 정보를 몇 번의 대화 동안 유지할지 결정하는 설정값
MAX_RELATION_CONTEXT_TURNS = 5

# 플레이어-NPC 조합에 대한 Redis 저장 키를 생성하는 함수
def build_relation_context_key(player_id: str, npc_id: str) -> str:
    return f"npc_relation_context:{player_id}:{npc_id}"

# 조회한 NPC 관계 정보를 redis에 저장하고 유지 횟수를 초기화
# 만약 대화 도중에 NPC 이름이 다시 언급된 경우 MAX_RELATION_CONTEXT_TURNS 만큼 갱신
def save_npc_relation_context(player_id: str, npc_id: str, relations: list[dict]):
    if not relations:
        return

    key = build_relation_context_key(player_id, npc_id)

    payload = {
        "remaining_turns": MAX_RELATION_CONTEXT_TURNS,
        "relations": relations
    }

    redis_client.set(key, json.dumps(payload, ensure_ascii=False))

# redis에서 NPC 관계 정보를 불러오고, 횟수를 감소시키며 만료 시 삭제
def get_npc_relation_context(player_id: str, npc_id: str):
    key = build_relation_context_key(player_id, npc_id)

    raw = redis_client.get(key)
    if not raw:
        return []

    payload = json.loads(raw)
    remaining_turns = payload.get("remaining_turns", 0)

    if remaining_turns <= 0:
        redis_client.delete(key)
        return []

    payload["remaining_turns"] = remaining_turns - 1
    redis_client.set(key, json.dumps(payload, ensure_ascii=False))

    return payload.get("relations", [])

# 관련 NPC 관계를 redis에서 삭제(대화 종료 시 작동)
def clear_npc_relation_context(player_id: str, npc_id: str):
    key = build_relation_context_key(player_id, npc_id)
    redis_client.delete(key)

# NPC 관계 정보를 LLM 프롬프트에 넣기 위한 문자열 형태로 변환
def npc_relations_to_text(relations: list[dict]):
    if not relations:
        return "No mentioned NPC relationship context."

    lines = []

    for rel in relations:
        lines.append(
            f"- {rel.get('source_npc_id')} knows {rel.get('target_name')}({rel.get('target_npc_id')}):\n"
            f"  job: {rel.get('target_job')}\n"
            f"  faction: {rel.get('target_faction')}\n"
            f"  personality: {rel.get('target_personality')}\n"
            f"  affinity: {rel.get('affinity')}\n"
            f"  trust: {rel.get('trust')}\n"
            f"  view: {rel.get('view_of_npc')}"
        )

    return "\n".join(lines)
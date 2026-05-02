import json
from core.redis import redis_client

MAX_RELATION_CONTEXT_TURNS = 5

def build_relation_context_key(player_id: str, npc_id: str) -> str:
    return f"npc_relation_context:{player_id}:{npc_id}"

def save_npc_relation_context(player_id: str, npc_id: str, relations: list[dict]):
    if not relations:
        return

    key = build_relation_context_key(player_id, npc_id)

    payload = {
        "remaining_turns": MAX_RELATION_CONTEXT_TURNS,
        "relations": relations
    }

    redis_client.set(key, json.dumps(payload, ensure_ascii=False))

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

def clear_npc_relation_context(player_id: str, npc_id: str):
    key = build_relation_context_key(player_id, npc_id)
    redis_client.delete(key)

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
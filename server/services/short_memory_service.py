# Redis를 사용해 최근 대화 기록을 저장 및 로드
import json
from core.redis import redis_client

MAX_SHORT_MEMORY_COUNT = 10

# 플레이어와 NPC 조합으로 Redis key를 만듦
def build_short_memory_key(player_id: str, npc_id: str) -> str:
    return f"short_memory:{player_id}:{npc_id}"

# 최근 대화 하나를 Redis에 저장
def save_message(player_id: str, npc_id: str, role: str, text: str):
    key = build_short_memory_key(player_id, npc_id)

    print("SAVE REDIS KEY:", key)

    message = {
        "role": role,
        "text": text
    }

    redis_client.rpush(key, json.dumps(message, ensure_ascii=False))

# 최근 대화 기록을 Redis에서 불러옴
def get_recent_messages(player_id: str, npc_id: str):
    key = build_short_memory_key(player_id, npc_id)

    raw_messages = redis_client.lrange(key, -MAX_SHORT_MEMORY_COUNT, -1)

    messages = []

    for raw in raw_messages:
        messages.append(json.loads(raw))

    return messages

# LLM 프롬프트에 넣기 좋게 최근 대화를 문자열 변환
def get_recent_messages_text(player_id: str, npc_id: str):
    messages = get_recent_messages(player_id, npc_id)

    if not messages:
        return "No recent conversation."

    lines = []

    for msg in messages:
        role = msg.get("role", "unknown")
        text = msg.get("text", "")

        if role == "user":
            lines.append(f"Player: {text}")
        elif role == "npc":
            lines.append(f"NPC: {text}")
        else:
            lines.append(f"{role}: {text}")

    return "\n".join(lines)

# 필요할 때 해당 NPC와의 단기 기억을 삭제한다.
def clear_short_memory(player_id: str, npc_id: str):
    key = build_short_memory_key(player_id, npc_id)

    print("CLEAR REDIS KEY:", key)

    deleted_count = redis_client.delete(key)

    print("DELETED REDIS COUNT:", deleted_count)
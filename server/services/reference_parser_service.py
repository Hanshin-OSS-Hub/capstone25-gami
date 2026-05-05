# LLM A_2 : 플레이어 발화에 들어있는 NPC 이름, episodic memory에 조회하는 태그 파싱
import json
from openai import OpenAI
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# 시스템에서 인식 가능한 NPC id 목록
KNOWN_NPC_IDS = ["bob", "rex", "jack", "alice"]

# id별로 다양한 이름, 별명, 직업 표현을 매핑한 사전
NPC_ALIAS_MAP = {
    "rex": ["rex", "렉스", "대장장이", "거친 대장장이"],
    "jack": ["jack", "잭", "상인", "장사꾼", "말 많은 상인"],
    "alice": ["alice", "앨리스", "학생", "아카데미 학생"],
    "bob": ["bob", "밥", "마법사", "길드 마법사"]
}

# episodic memory 조회에 사용되는 태그 목록
KNOWN_EVENT_TAGS = [
    "rex",
    "jack",
    "alice",
    "bob",
    "trade",
    "conflict",
    "guild",
    "magic",
    "academy",
    "blacksmith"
]

# 태그별 다양한 표현을 매핑한 사전
TAG_ALIAS_MAP = {
    "trade": ["trade", "거래", "장사", "납품", "대금"],
    "conflict": ["conflict", "갈등", "싸움", "다툼"],
    "guild": ["guild", "길드"],
    "magic": ["magic", "마법"],
    "academy": ["academy", "아카데미"],
    "blacksmith": ["blacksmith", "대장장이"]
}

# LLM 사용하지 않고 언급된 NPC id 추출
def parse_npcs_with_rules(user_text: str, current_npc_id: str) -> list[str]:
    text = user_text.lower()
    result = []

    for npc_id, aliases in NPC_ALIAS_MAP.items():
        if npc_id == current_npc_id:
            continue

        for alias in aliases:
            if alias.lower() in text:
                result.append(npc_id)
                break

    return list(set(result))

# LLM 사용하지 않고 언급된 episodic memory 태그 파싱
def parse_tags_with_rules(user_text: str) -> list[str]:
    text = user_text.lower()
    result = []

    for tag, aliases in TAG_ALIAS_MAP.items():
        for alias in aliases:
            if alias.lower() in text:
                result.append(tag)
                break

    return list(set(result))

# LLM을 통해 NPC id와 episodic memory 태그 파싱 (LLM A_2)
def parse_with_llm(user_text: str, current_npc_id: str) -> dict:
    prompt = f"""
Extract NPC references and event memory tags from the player's message.

Current speaking NPC:
{current_npc_id}

Known NPCs:
- rex: blacksmith, rough personality
- jack: merchant, talkative
- alice: academy student
- bob: wizard

Known event tags:
{KNOWN_EVENT_TAGS}

Player message:
"{user_text}"

Return ONLY valid JSON:
{{
  "mentioned_npc_ids": [],
  "event_tags": []
}}

Rules:
- Do not include the current speaking NPC in mentioned_npc_ids.
- mentioned_npc_ids must only contain known NPC ids.
- event_tags must only contain known event tags.
- If nothing is clearly referenced, return empty lists.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You extract references from text. Return JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)

        mentioned_npc_ids = [
            npc_id for npc_id in data.get("mentioned_npc_ids", [])
            if npc_id in KNOWN_NPC_IDS and npc_id != current_npc_id
        ]

        event_tags = [
            tag for tag in data.get("event_tags", [])
            if tag in KNOWN_EVENT_TAGS
        ]

        return {
            "mentioned_npc_ids": mentioned_npc_ids,
            "event_tags": event_tags
        }

    except Exception:
        return {
            "mentioned_npc_ids": [],
            "event_tags": []
        }

# 함수를 통한 파싱을 우선 수행하고, 실패했을 경우 LLM을 통해 파싱 시도
def parse_references(user_text: str, current_npc_id: str) -> dict:
    mentioned_npc_ids = parse_npcs_with_rules(user_text, current_npc_id)
    event_tags = parse_tags_with_rules(user_text)

    if mentioned_npc_ids or event_tags:
        return {
            "mentioned_npc_ids": mentioned_npc_ids,
            "event_tags": event_tags
        }

    return parse_with_llm(user_text, current_npc_id)
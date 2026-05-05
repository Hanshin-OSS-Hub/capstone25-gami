# LLM A_1 : 플레이어 발화 분석
from openai import OpenAI
from core.config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

# LLM이 반환한 변화량(delta)을 -10 ~ 10 범위로 제한
def clamp_delta(value, min_value = -10, max_value = 10):
    try:
        value = int(value)
    except Exception:
        return 0

    return max(min_value, min(max_value, value))


# LLM A_1이 플레이어 발화를 분석해 NPC 상태 변화량(affinity, trust, mood)과 인식 변화를 계산
def analyze_player_text(user_text: str, state_memory: dict, recent_dialogue_text: str = "") -> dict:
    prompt = f"""
        You are responsible for analyzing how a player's message affects an NPC's internal state.

        Do NOT reduce the message to a single simple label such as "compliment" or "insult".
        Instead, analyze the full meaning of the message, including mixed or contradictory tones.

        Current NPC state:
        - Affinity (liking toward player): {state_memory.get("affinity", 0)}
        - Trust (trust toward player): {state_memory.get("trust", 0)}
        - Mood (current emotional state): {state_memory.get("mood", 0)}
        - View of player: {state_memory.get("view_of_player", "")}

        Recent conversation:
        {recent_dialogue_text}

        Current player message:
        {user_text}

        Rules:
        - Each state value is in range -100 to 100.
        - Return DELTA values, not absolute values.
        - Each delta must be an integer between -10 and 10.
        - If the message does not meaningfully affect the NPC's relationship or mood, return 0.
        - Do not change values just because the player said something.
        - Small talk, factual questions, or neutral statements should usually produce 0 delta.
        - Use larger deltas only for emotionally meaningful actions such as sincere praise, insult, threat, betrayal, apology, help, or important promises.
        - Consider nuance: a message may contain both positive and negative elements.
        - Do not exaggerate small casual interactions.

        Return ONLY valid JSON.

        Output format:
        {{
        "affinity_delta": 0,
        "trust_delta": 0,
        "mood_delta": 0,
        "view_of_player_update": "Short sentence describing how the NPC now perceives the player",
        "reason": "Short explanation of your reasoning"
        }}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON-only analyzer. Do not output anything except valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw_text)
    except Exception:
        return {
            "affinity_delta": 0,
            "trust_delta": 0,
            "mood_delta": 0,
            "view_of_player_update": state_memory.get("view_of_player", ""),
            "reason": "JSON 파싱 실패로 상태 변화 없음"
        }

    return {
        "affinity_delta": clamp_delta(result.get("affinity_delta", 0)),
        "trust_delta": clamp_delta(result.get("trust_delta", 0)),
        "mood_delta": clamp_delta(result.get("mood_delta", 0)),
        "view_of_player_update": result.get(
            "view_of_player_update",
            state_memory.get("view_of_player", "")
        ),
        "reason": result.get("reason", "")
    }
# LLM B가 최종 NPC 응답을 생성

from openai import OpenAI
from core.config import OPENAI_API_KEY
from services.semantic_memory_service import get_semantic_memory_text

client = OpenAI(api_key=OPENAI_API_KEY)


# 호감도(정량 수치)에 따른 정성적 문구 생성
def affinity_to_text(value: int):
    if value <= -4:
        return "strongly dislikes the player"
    elif value <= -2:
        return "dislikes the player"
    elif value < 0:
        return "is slightly negative toward the player"
    elif value == 0:
        return "feels neutral toward the player"
    elif value <= 2:
        return "is slightly friendly toward the player"
    elif value <= 4:
        return "likes the player"
    else:
        return "greatly likes the player"


# 신뢰도(정량 수치)에 따른 정성적 문구 생성
def trust_to_text(value: int):
    if value <= -4:
        return "does not trust the player at all"
    elif value <= -2:
        return "distrusts the player"
    elif value < 0:
        return "is slightly suspicious of the player"
    elif value == 0:
        return "has no particular trust in the player"
    elif value <= 2:
        return "trusts the player a little"
    elif value <= 4:
        return "trusts the player"
    else:
        return "completely trusts the player"


# 기분(정량 수치)에 따른 정성적 문구 생성
def mood_to_text(value: int):
    if value <= -4:
        return "in a very bad mood"
    elif value <= -2:
        return "in a bad mood"
    elif value < 0:
        return "slightly irritated"
    elif value == 0:
        return "in a normal mood"
    elif value <= 2:
        return "in a good mood"
    elif value <= 4:
        return "in a very good mood"
    else:
        return "extremely cheerful"


# 최종 답변을 요구하는 프롬포트
def generate_npc_response(
    npc_id: str,
    player_id: str,
    user_text: str,
    state_memory: dict,
    analysis_result: dict
) -> str:
    semantic_memory_text = get_semantic_memory_text()
    affinity_text = affinity_to_text(state_memory["affinity"])
    trust_text = trust_to_text(state_memory["trust"])
    mood_text = mood_to_text(state_memory["mood"])

    system_prompt = (
        f"You are an NPC in a game.\n\n"

        f"NPC profile:\n"
        f"- NPC ID: {state_memory.get('npc_id', npc_id)}\n"
        f"- Name: {state_memory.get('name', '')}\n"
        f"- Age: {state_memory.get('age', '')}\n"
        f"- Gender: {state_memory.get('gender', '')}\n"
        f"- Job: {state_memory.get('job', '')}\n"
        f"- Faction: {state_memory.get('faction', '')}\n"
        f"- Speech style: {state_memory.get('speech_style', '')}\n"
        f"- Personality: {state_memory.get('personality', '')}\n\n"

        f"Player info:\n"
        f"- Player ID: {player_id}\n\n"

        f"NPC state memory toward player:\n"
        f"NPC current state:\n"
        f"The NPC {affinity_text}.\n"
        f"The NPC {trust_text}.\n"
        f"The NPC is currently {mood_text}.\n"
        f"The NPC thinks of the player as: {state_memory.get('view_of_player','')}\n\n"

        f"Semantic memory:\n"
        f"{semantic_memory_text}\n\n"

        f"Analysis result of player's latest message:\n"
        f"- Intent: {analysis_result.get('intent', 'unknown')}\n"
        f"- Emotion: {analysis_result.get('emotion', 'neutral')}\n"
        f"- Affinity delta: {analysis_result.get('affinity_delta', 0)}\n\n"

        f"Instructions:\n"
        f"- Reply as the NPC naturally.\n"
        f"- Reflect the NPC's speech style and personality.\n"
        f"- Reflect the NPC's current state toward the player.\n"
        f"- Do not explain the state values directly unless necessary.\n"
        f"- Stay consistent with the semantic memory."
    )

    print("STATE MEMORY:", state_memory)
    print("SYSTEM PROMPT:\n", system_prompt)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response.choices[0].message.content.strip()
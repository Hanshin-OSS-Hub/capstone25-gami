# LLM B가 최종 NPC 응답을 생성

from openai import OpenAI
from core.config import OPENAI_API_KEY
from services.semantic_memory_service import get_semantic_memory_text

client = OpenAI(api_key=OPENAI_API_KEY)


# 호감도(정량 수치)에 따른 정성적 문구 생성
def affinity_to_text(value: int):
    if value <= -80:
        return "strongly hates the player"
    elif value <= -50:
        return "strongly dislikes the player"
    elif value <= -20:
        return "dislikes the player"
    elif value < 0:
        return "is slightly negative toward the player"
    elif value == 0:
        return "feels neutral toward the player"
    elif value < 20:
        return "is slightly friendly toward the player"
    elif value < 50:
        return "likes the player"
    elif value < 80:
        return "strongly likes the player"
    else:
        return "deeply cares about the player"



# 신뢰도(정량 수치)에 따른 정성적 문구 생성
def trust_to_text(value: int):
    if value <= -80:
        return "believes the player is extremely untrustworthy"
    elif value <= -50:
        return "does not trust the player at all"
    elif value <= -20:
        return "distrusts the player"
    elif value < 0:
        return "is slightly suspicious of the player"
    elif value == 0:
        return "has no particular trust in the player"
    elif value < 20:
        return "trusts the player a little"
    elif value < 50:
        return "trusts the player"
    elif value < 80:
        return "strongly trusts the player"
    else:
        return "trusts the player completely"


# 기분(정량 수치)에 따른 정성적 문구 생성
def mood_to_text(value: int):
    if value <= -80:
        return "in an extremely bad mood"
    elif value <= -50:
        return "in a very bad mood"
    elif value <= -20:
        return "in a bad mood"
    elif value < 0:
        return "slightly irritated"
    elif value == 0:
        return "in a normal mood"
    elif value < 20:
        return "in a slightly good mood"
    elif value < 50:
        return "in a good mood"
    elif value < 80:
        return "in a very good mood"
    else:
        return "extremely cheerful"


# 최종 답변을 요구하는 프롬포트
def generate_npc_response(
    npc_id: str,
    player_id: str,
    user_text: str,
    state_memory: dict,
    analysis_result: dict, 
    recent_dialogue_text: str,
    npc_relation_context_text: str,
    event_memory_text: str
) -> str:
    semantic_memory_text = get_semantic_memory_text()
    affinity_text = affinity_to_text(state_memory["affinity"])
    trust_text = trust_to_text(state_memory["trust"])
    mood_text = mood_to_text(state_memory["mood"])

    system_prompt = (
        f"You are an NPC in a game.\n"
        f"Do not end responses in plain sentence form unless absolutely necessary.\n"
        f"Only provide responses that fit the established world setting.\n"
        f"If a topic does not align with the world setting, deflect or reinterpret it in a way that remains consistent with the world.\n\n"

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

        f"Recent conversation:\n"
        f"{recent_dialogue_text}\n\n"

        f"Mentioned NPC relationship context:\n"
        f"{npc_relation_context_text}\n\n"

        f"Relevant event memory:\n"
        f"{event_memory_text}\n\n"
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
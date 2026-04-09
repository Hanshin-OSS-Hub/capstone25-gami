from services.analysis_service import analyze_player_text
from services.state_memory_service import ensure_session_state, update_session_state
from services.response_service import generate_npc_response

def process_dialogue(npc_id: str, player_id: str, user_text: str) -> str:
    state = ensure_session_state(player_id, npc_id)

    analysis_result = analyze_player_text(user_text)

    updated_state = update_session_state(
        player_id,
        npc_id,
        {
            "affinity": state["affinity"] + analysis_result.get("affinity_delta", 0),
            "trust": state["trust"],
            "view_of_player": state["view_of_player"]
        }
    )

    npc_text = generate_npc_response(
        npc_id=npc_id,
        player_id=player_id,
        user_text=user_text,
        state_memory=updated_state,
        analysis_result=analysis_result
    )

    return npc_text
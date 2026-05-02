from services.analysis_service import analyze_player_text
from services.state_memory_service import ensure_session_state, update_session_state
from services.response_service import generate_npc_response
from services.short_memory_service import get_recent_messages_text, save_message
from services.reference_parser_service import parse_references
from repositories.npc_relation_repository import load_npc_relations_from_neo4j
from services.npc_relation_context_service import (
    save_npc_relation_context,
    get_npc_relation_context,
    npc_relations_to_text
)
from services.semantic_memory_service import (
    get_event_memory_by_tags,
    event_memory_to_text
)


def clamp_state(value, min_value=-100, max_value=100):
    try:
        value = int(value)
    except Exception:
        return 0

    return max(min_value, min(max_value, value))


def process_dialogue(npc_id: str, player_id: str, user_text: str) -> str:
    state = ensure_session_state(player_id, npc_id)

    recent_dialogue_text = get_recent_messages_text(player_id, npc_id)

    references = parse_references(
        user_text=user_text,
        current_npc_id=npc_id
    )

    mentioned_npc_ids = references["mentioned_npc_ids"]
    event_tags = references["event_tags"]

    if mentioned_npc_ids:
        fresh_relations = load_npc_relations_from_neo4j(
            source_npc_id=npc_id,
            target_npc_ids=mentioned_npc_ids
        )
        save_npc_relation_context(player_id, npc_id, fresh_relations)

    npc_relation_context = get_npc_relation_context(player_id, npc_id)
    npc_relation_context_text = npc_relations_to_text(npc_relation_context)

    event_memories = get_event_memory_by_tags(event_tags)
    event_memory_text = event_memory_to_text(event_memories)

    analysis_result = analyze_player_text(
        user_text=user_text,
        state_memory=state,
        recent_dialogue_text=recent_dialogue_text
    )

    analysis_result["mentioned_npc_ids"] = mentioned_npc_ids
    analysis_result["event_tags"] = event_tags

    updated_state = update_session_state(
        player_id,
        npc_id,
        {
            "affinity": clamp_state(state["affinity"] + analysis_result.get("affinity_delta", 0)),
            "trust": clamp_state(state["trust"] + analysis_result.get("trust_delta", 0)),
            "mood": clamp_state(state["mood"] + analysis_result.get("mood_delta", 0)),
            "view_of_player": analysis_result.get("view_of_player_update", state["view_of_player"])
        }
    )

    npc_text = generate_npc_response(
        npc_id=npc_id,
        player_id=player_id,
        user_text=user_text,
        state_memory=updated_state,
        analysis_result=analysis_result,
        recent_dialogue_text=recent_dialogue_text,
        npc_relation_context_text=npc_relation_context_text,
        event_memory_text=event_memory_text
    )

    save_message(player_id, npc_id, "user", user_text)
    save_message(player_id, npc_id, "npc", npc_text)

    return npc_text
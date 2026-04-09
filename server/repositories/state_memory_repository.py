# Neo4j에서 state memory를 읽고 저장하는 쿼리를 담당

from core.neo4j import driver

# Player-NPC 관계에서 state memory를 읽어옴
def load_state_memory_from_neo4j(player_id: str, npc_id: str):
    query = """
    MATCH (n:NPC {id: $npc_id})
    MERGE (p:Player {id: $player_id})
    MERGE (p)-[r:KNOWS]->(n)
    ON CREATE SET
        r.affinity = 0,
        r.trust = 0,
        r.view_of_player = "플레이어를 처음 본 상태이며 아직 뚜렷한 인상이 없다."
    RETURN
        n.id AS npc_id,
        p.id AS player_id,
        n.name AS name,
        n.age AS age,
        n.gender AS gender,
        n.job AS job,
        n.faction AS faction,
        n.speech_style AS speech_style,
        n.personality AS personality,
        r.affinity AS affinity,
        r.trust AS trust,
        r.view_of_player AS view_of_player
    """

    with driver.session() as session:
        record = session.run(
            query,
            player_id=player_id,
            npc_id=npc_id
        ).single()

        if record is None:
            return None

        return {
            "npc_id": record["npc_id"],
            "player_id": record["player_id"],
            "name": record["name"],
            "age": record["age"],
            "gender": record["gender"],
            "job": record["job"],
            "faction": record["faction"],
            "speech_style": record["speech_style"],
            "personality": record["personality"],
            "affinity": record["affinity"],
            "trust": record["trust"],
            "view_of_player": record["view_of_player"],
        }

# FastAPI 메모리에 있는 state memory를 Neo4j에 저장
def save_state_memory_to_neo4j(
    player_id: str,
    npc_id: str,
    affinity: int,
    trust: int,
    view_of_player: str
):
    query = """
    MATCH (n:NPC {id: $npc_id})
    MERGE (p:Player {id: $player_id})
    MERGE (p)-[r:KNOWS]->(n)
    SET
        r.affinity = $affinity,
        r.trust = $trust,
        r.view_of_player = $view_of_player
    """

    with driver.session() as session:
        session.run(
            query,
            npc_id=npc_id,
            player_id=player_id,
            affinity=affinity,
            trust=trust,
            view_of_player=view_of_player
        )
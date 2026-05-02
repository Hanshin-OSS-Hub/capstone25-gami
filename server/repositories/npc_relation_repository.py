from core.neo4j import driver

def load_npc_relations_from_neo4j(source_npc_id: str, target_npc_ids: list[str]):
    if not target_npc_ids:
        return []

    query = """
    MATCH (source:NPC {id: $source_npc_id})
    MATCH (target:NPC)
    WHERE target.id IN $target_npc_ids
    OPTIONAL MATCH (source)-[r:KNOWS_NPC]->(target)
    RETURN
        source.id AS source_npc_id,
        target.id AS target_npc_id,
        target.name AS target_name,
        target.job AS target_job,
        target.faction AS target_faction,
        target.personality AS target_personality,
        r.affinity AS affinity,
        r.trust AS trust,
        r.view_of_npc AS view_of_npc
    """

    with driver.session() as session:
        records = session.run(
            query,
            source_npc_id=source_npc_id,
            target_npc_ids=target_npc_ids
        )

        result = []

        for record in records:
            result.append({
                "source_npc_id": record["source_npc_id"],
                "target_npc_id": record["target_npc_id"],
                "target_name": record["target_name"],
                "target_job": record["target_job"],
                "target_faction": record["target_faction"],
                "target_personality": record["target_personality"],
                "affinity": record["affinity"],
                "trust": record["trust"],
                "view_of_npc": record["view_of_npc"],
            })

        return result
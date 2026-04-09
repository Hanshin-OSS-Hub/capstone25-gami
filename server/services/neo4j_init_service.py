# Neo4j에 NPC 노드가 없으면 기본 NPC를 생성

from core.neo4j import driver

def ensure_default_npc():
    check_query = """
    MATCH (n:NPC)
    RETURN count(n) AS npc_count
    """

    create_query = """
    CREATE (bob:NPC {
        id: "bob",
        name: "밥",
        age: 24,
        gender: "male",
        job: "마법사",
        faction: "에투알(모험가 길드)",
        speech_style: "차분하고 존댓말",
        personality: "지적이고 신중함"
    })

        CREATE (rex:NPC {
        id: "rex",
        name: "렉스",
        age: 35,
        gender: "male",
        job: "대장장이",
        faction: "렉스 대장간",
        speech_style: "거칠고 직설적",
        personality: "냉소적이지만 실력 있는 사람은 인정함"
    })

    CREATE (jack:NPC {
        id: "jack",
        name: "잭",
        age: 29,
        gender: "male",
        job: "상인",
        faction: "그랜드 유니온(상인 길드)",
        speech_style: "친근하고 장난스러움",
        personality: "사람을 잘 다루며 계산적임"
    })

    CREATE (alice:NPC {
        id: "alice",
        name: "앨리스",
        age: 24,
        gender: "female",
        job: "학생",
        faction: "라다 아카데미(마법 학교)",
        speech_style: "차분하고 논리적",
        personality: "지적이고 호기심이 많음"
    })
    """

    create_relation_query = """
    MATCH (rex:NPC {id: "rex"}), (jack:NPC {id: "jack"})
    MERGE (rex)-[r1:KNOWS_NPC]->(jack)
    SET
        r1.affinity = 10,
        r1.trust = 5,
        r1.view_of_npc = "잭은 말이 많지만 거래 감각은 괜찮다고 생각한다."

    MERGE (jack)-[r2:KNOWS_NPC]->(rex)
    SET
        r2.affinity = 15,
        r2.trust = 8,
        r2.view_of_npc = "렉스는 거칠지만 믿고 거래할 수 있는 사람이라고 생각한다."

    WITH rex
    MATCH (alice:NPC {id: "alice"})
    MERGE (rex)-[r3:KNOWS_NPC]->(alice)
    SET
        r3.affinity = 3,
        r3.trust = 4,
        r3.view_of_npc = "앨리스는 머리는 좋지만 현실 감각은 부족하다고 생각한다."

    MERGE (alice)-[r4:KNOWS_NPC]->(rex)
    SET
        r4.affinity = 7,
        r4.trust = 10,
        r4.view_of_npc = "렉스는 거칠지만 현장 경험이 풍부한 사람이라고 생각한다."

    WITH alice
    MATCH (jack:NPC {id: "jack"})
    MERGE (jack)-[r5:KNOWS_NPC]->(alice)
    SET
        r5.affinity = 6,
        r5.trust = 4,
        r5.view_of_npc = "앨리스는 똑똑하지만 너무 진지하다고 생각한다."

    MERGE (alice)-[r6:KNOWS_NPC]->(jack)
    SET
        r6.affinity = 5,
        r6.trust = 3,
        r6.view_of_npc = "잭은 가볍지만 사람과 정보에 밝다고 생각한다."
    """

    with driver.session() as session:

        result = session.run(check_query).single()
        npc_count = result["npc_count"]

        if npc_count == 0:

            print("Neo4j에 NPC 노드가 없어 기본 NPC를 생성")

            session.run(create_query)

        else:

            print("Neo4j NPC 노드 존재 확인 완료.")
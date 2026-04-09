# MongoDB의 semantic_memory 컬렉션에서 실제 데이터를 읽어오는 역할

from core.mongodb import mongo_db

# MongoDB의 semantic_memory 컬렉션에서 모든 문서를 읽어옴
def fetch_all_semantic_memory():
    return list(
        mongo_db.semantic_memory.find(
            {},
            {"_id": 0}
        )
    )
from repositories.semantic_memory_repository import fetch_all_semantic_memory

# MongoDB에서 읽은 semantic memory를 서버 메모리에 캐시하는 변수
_semantic_memory_cache = None

# MongoDB의 semantic_memory 컬렉션에서 모든 데이터를 읽어와 캐시에 저장
def load_semantic_memory():
    global _semantic_memory_cache

    docs = fetch_all_semantic_memory()
    _semantic_memory_cache = docs
    return _semantic_memory_cache

# 이미 캐시가 있으면 캐시를 반환하고, 없으면 MongoDB에서 최초 1회 로드
def get_semantic_memory():
    global _semantic_memory_cache

    if _semantic_memory_cache is None:
        load_semantic_memory()

    return _semantic_memory_cache

# MongoDB에서 semantic memory를 다시 읽어와 캐시를 갱신
def reload_semantic_memory():
    return load_semantic_memory()

# LLM 프롬프트에 넣기 위해 semantic memory를 문자열로 변환
def get_semantic_memory_text():
    memories = get_semantic_memory()

    if not memories:
        return "세계관 정보 없음"

    lines = []

    for memory in memories:
        title = memory.get("title", "제목 없음")
        content = memory.get("content", "")
        lines.append(f"{title}: {content}")

    return "\n".join(lines)
from repositories.semantic_memory_repository import (
    fetch_all_semantic_memory,
    fetch_semantic_memory_by_tags
)

_semantic_memory_cache = None

# MongoDB에서 전체 semantic memory를 읽어와 캐시에 저장
def load_semantic_memory():
    global _semantic_memory_cache

    docs = fetch_all_semantic_memory()
    _semantic_memory_cache = docs
    return _semantic_memory_cache

# 캐시된 semantic memory를 반환하되 없으면 최초 1회 로드
def get_semantic_memory():
    global _semantic_memory_cache

    if _semantic_memory_cache is None:
        load_semantic_memory()

    return _semantic_memory_cache

# MongoDB에서 semantic memory를 다시 불러와 캐시를 갱신
def reload_semantic_memory():
    return load_semantic_memory()

# 전체 semantic memory를 LLM 프롬프트용 문자열로 변환
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

# 특정 태그 기반으로 이벤트 memory를 MongoDB에서 조회
def get_event_memory_by_tags(tags: list[str]):
    return fetch_semantic_memory_by_tags(tags)

# 조회된 이벤트 memory를 LLM 프롬프트용 문자열로 변환
def event_memory_to_text(memories: list[dict]):
    if not memories:
        return "No relevant event memory."

    lines = []

    for memory in memories:
        title = memory.get("title", "Untitled event")
        content = memory.get("content", "")
        lines.append(f"- {title}: {content}")

    return "\n".join(lines)
from repositories.semantic_memory_repository import (
    fetch_all_semantic_memory,
    fetch_semantic_memory_by_tags
)

_semantic_memory_cache = None


def load_semantic_memory():
    global _semantic_memory_cache

    docs = fetch_all_semantic_memory()
    _semantic_memory_cache = docs
    return _semantic_memory_cache


def get_semantic_memory():
    global _semantic_memory_cache

    if _semantic_memory_cache is None:
        load_semantic_memory()

    return _semantic_memory_cache


def reload_semantic_memory():
    return load_semantic_memory()


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


def get_event_memory_by_tags(tags: list[str]):
    return fetch_semantic_memory_by_tags(tags)


def event_memory_to_text(memories: list[dict]):
    if not memories:
        return "No relevant event memory."

    lines = []

    for memory in memories:
        title = memory.get("title", "Untitled event")
        content = memory.get("content", "")
        lines.append(f"- {title}: {content}")

    return "\n".join(lines)
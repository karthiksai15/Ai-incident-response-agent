from app.memory.embedding import (
    create_memory_embedding,
    create_memory_text,
)
from app.memory.relevance import filter_relevant_memories
from app.memory.vector_store import IncidentMemoryVectorStore


def retrieve_similar_incidents(
    service: str,
    severity: str,
    evidence: list[str],
    top_k: int = 3,
) -> list[dict]:

    text = create_memory_text(
        service=service,
        severity=severity,
        root_cause="",
        evidence=evidence,
    )

    embedding = create_memory_embedding(text)

    vector_store = IncidentMemoryVectorStore()

    candidate_memories = vector_store.search(
        embedding=embedding,
        top_k=max(top_k * 2, 5),
    )

    relevant_memories = filter_relevant_memories(
        memories=candidate_memories,
        service=service,
        severity=severity,
    )

    return relevant_memories[:top_k]

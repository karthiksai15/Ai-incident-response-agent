from app.memory.retrieval import retrieve_similar_incidents
from app.models.knowledge import KnowledgeContext
from app.memory.runbook_retrieval import retrieve_runbook_knowledge


def retrieve_combined_knowledge(
    service: str,
    severity: str,
    evidence: list[str],
    top_k: int = 3,
) -> KnowledgeContext:

    memory_results = retrieve_similar_incidents(
        service=service,
        severity=severity,
        evidence=evidence,
        top_k=top_k,
    )

    memory_context = [
        result["document"]
        for result in memory_results
    ]

    runbook_context = retrieve_runbook_knowledge(
        service=service,
        severity=severity,
        evidence=evidence,
        top_k=top_k,
    )

    return KnowledgeContext(
        runbooks=runbook_context,
        similar_incidents=memory_context,
    )

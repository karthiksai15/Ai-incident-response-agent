from app.agents.rag_executor import retrieve_incident_knowledge


def retrieve_runbook_knowledge(
    service: str,
    severity: str,
    evidence: list[str],
    top_k: int = 3,
) -> list[str]:

    query = " ".join(
        [
            service,
            severity,
            *evidence,
        ]
    )

    return retrieve_incident_knowledge(
        query=query,
        top_k=top_k,
    )

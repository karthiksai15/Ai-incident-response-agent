from app.agents.prompts import (
    build_incident_analysis_prompt,
    build_memory_rag_analysis_prompt,
)
from app.agents.structured_llm import analyze_with_llm


def analyze_investigation(
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
    retrieved_knowledge: list[str],
):
    prompt = build_incident_analysis_prompt(
        incident_id=incident_id,
        service=service,
        severity=severity,
        evidence=evidence,
        retrieved_knowledge=retrieved_knowledge,
    )

    return analyze_with_llm(
        prompt=prompt,
    )


def analyze_memory_rag_investigation(
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
    runbooks: list[str],
    similar_incidents: list[str],
):
    prompt = build_memory_rag_analysis_prompt(
        incident_id=incident_id,
        service=service,
        severity=severity,
        evidence=evidence,
        runbooks=runbooks,
        similar_incidents=similar_incidents,
    )

    return analyze_with_llm(
        prompt=prompt,
    )

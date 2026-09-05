from app.agents.prompts import (
    build_incident_analysis_prompt,
)
from app.agents.structured_llm import (
    analyze_with_llm,
)
from app.graph.state import IncidentState


def analyze_evidence(state: IncidentState):
    prompt = build_incident_analysis_prompt(
        incident_id=state["incident_id"],
        service=state["service"],
        severity=state["severity"],
        evidence=state["evidence"],
        retrieved_knowledge=state["retrieved_knowledge"],
    )

    analysis = analyze_with_llm(
        prompt=prompt,
    )

    return {
        "root_cause": analysis.root_cause,
        "confidence": analysis.confidence,
        "recommendation": analysis.recommendation,
        "investigation_notes": [
            "Incident analyzed using the Gemini LLM."
        ],
    }

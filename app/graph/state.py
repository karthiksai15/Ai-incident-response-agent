from typing import TypedDict


class IncidentState(TypedDict):
    incident_id: str
    service: str
    severity: str

    logs: list[str]
    evidence: list[str]
    retrieved_knowledge: list[str]
    similar_incidents: list[str]

    root_cause: str
    confidence: float
    recommendation: str

    investigation_notes: list[str]

    # Agent decision-loop state
    current_goal: str
    completed_goals: list[str]

    next_action: str
    tools_used: list[str]
    iteration: int
    investigation_complete: bool

from app.agents.agent_controller import run_agent_investigation
from app.graph.state import IncidentState


def build_agent_state(
    incident: dict,
) -> IncidentState:
    """
    Convert an evaluation incident into the state
    required by the investigation agent.

    Ground-truth fields are intentionally excluded.
    """

    return IncidentState(
        incident_id=incident["incident_id"],
        service=incident["service"],
        severity=incident["severity"],
        logs=incident["logs"],
        evidence=[],
        retrieved_knowledge=[],
        similar_incidents=[],
        root_cause="",
        confidence=0.0,
        recommendation="",
        investigation_notes=[],
        current_goal="",
        completed_goals=[],
        next_action="",
        tools_used=[],
        iteration=0,
        investigation_complete=False,
    )


def run_agent_for_incident(
    incident: dict,
) -> dict:
    """
    Run the investigation agent for one evaluation incident.
    """

    state = build_agent_state(incident)

    result = run_agent_investigation(
        state=state,
        max_iterations=5,
    )

    return {
        "incident_id": result["incident_id"],
        "root_cause": result["root_cause"],
        "evidence": result["evidence"],
        "confidence": result["confidence"],
        "recommendation": result["recommendation"],
    }

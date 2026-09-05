from app.graph.state import IncidentState


def test_incident_state_contains_decision_fields():
    state: IncidentState = {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [],
        "retrieved_knowledge": [],
        "root_cause": "",
        "confidence": 0.0,
        "recommendation": "",
        "investigation_notes": [],
        "next_action": "check_service_health",
        "tools_used": [],
        "iteration": 0,
        "investigation_complete": False,
    }

    assert state["next_action"] == "check_service_health"
    assert state["tools_used"] == []
    assert state["iteration"] == 0
    assert state["investigation_complete"] is False

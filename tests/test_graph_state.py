from app.graph.state import IncidentState


def test_incident_state_structure():
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
    }

    assert state["incident_id"] == "INC-001"
    assert state["service"] == "payment-service"
    assert state["severity"] == "HIGH"
    assert state["root_cause"] == ""
    assert state["confidence"] == 0.0

from app.graph.incident_graph import incident_graph


def test_incident_graph():

    initial_state = {
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

    result = incident_graph.invoke(
        initial_state
    )

    assert result["incident_id"] == "INC-001"
    assert len(result["logs"]) > 0
    assert len(result["evidence"]) > 0
    assert len(result["retrieved_knowledge"]) > 0

    root_cause = result["root_cause"].lower()

    assert "database" in root_cause
    assert "connection" in root_cause
    assert "pool" in root_cause

    assert 0.0 <= result["confidence"] <= 1.0

    assert result["recommendation"] != ""

    assert any(
        "gemini" in note.lower()
        for note in result["investigation_notes"]
    )

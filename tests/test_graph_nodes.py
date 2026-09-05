from app.graph.nodes import (
    load_incident,
    extract_evidence,
)


def test_load_incident():
    state = {
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

    result = load_incident(state)

    assert "logs" in result
    assert len(result["logs"]) > 0


def test_extract_evidence():
    state = {
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

    result = extract_evidence(state)

    assert "evidence" in result
    assert len(result["evidence"]) > 0

    assert any(
        "connection pool exhausted" in evidence.lower()
        for evidence in result["evidence"]
    )

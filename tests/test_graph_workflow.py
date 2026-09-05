from app.graph.incident_graph import incident_graph


def create_initial_state():
    return {
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


def test_graph_state_propagation():
    result = incident_graph.invoke(
        create_initial_state()
    )

    assert result["incident_id"] == "INC-001"

    assert result["service"] == "payment-service"

    assert result["severity"] == "HIGH"

    assert len(result["logs"]) > 0

    assert len(result["evidence"]) > 0

    assert len(result["retrieved_knowledge"]) > 0


def test_graph_produces_analysis():
    result = incident_graph.invoke(
        create_initial_state()
    )

    assert result["root_cause"] != ""

    assert result["confidence"] > 0

    assert result["recommendation"] != ""

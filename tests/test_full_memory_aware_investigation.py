from app.agents import decision_executor
from app.graph import agent_workflow


def build_initial_state():
    return {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [],
        "retrieved_knowledge": [],
        "similar_incidents": [],
        "root_cause": "",
        "confidence": 0.0,
        "recommendation": "",
        "investigation_notes": [],
        "current_goal": "",
        "completed_goals": [],
        "next_action": "",
        "tools_used": [],
        "iteration": 0,
        "investigation_complete": False,
    }


def fake_retrieve_combined_knowledge(
    service,
    severity,
    evidence,
    top_k=3,
):
    assert service == "payment-service"
    assert severity == "HIGH"
    assert evidence
    assert top_k == 3

    return type(
        "KnowledgeContext",
        (),
        {
            "runbooks": [
                "Database connection pool exhaustion runbook."
            ],
            "similar_incidents": [
                "Previous database pool exhaustion incident."
            ],
        },
    )()


def fake_analyze_memory_rag_investigation(
    incident_id,
    service,
    severity,
    evidence,
    runbooks,
    similar_incidents,
):
    assert incident_id == "INC-001"
    assert service == "payment-service"
    assert severity == "HIGH"
    assert evidence
    assert runbooks
    assert similar_incidents

    return type(
        "Analysis",
        (),
        {
            "root_cause": "Database connection pool exhaustion",
            "confidence": 0.95,
            "recommendation": (
                "Investigate database connections and connection leaks."
            ),
            "evidence": [
                "Connection pool exhausted",
                "Timeout waiting for database connection",
            ],
        },
    )()


def test_full_memory_aware_investigation(monkeypatch):

    monkeypatch.setattr(
        decision_executor,
        "retrieve_combined_knowledge",
        fake_retrieve_combined_knowledge,
    )

    monkeypatch.setattr(
        decision_executor,
        "analyze_memory_rag_investigation",
        fake_analyze_memory_rag_investigation,
    )

    result = agent_workflow.agent_workflow.invoke(
        build_initial_state()
    )

    assert result["investigation_complete"] is True

    assert result["root_cause"] == (
        "Database connection pool exhaustion"
    )

    assert result["confidence"] == 0.95

    assert result["similar_incidents"] == [
        "Previous database pool exhaustion incident."
    ]

    assert "retrieve_knowledge" in result["completed_goals"]
    assert "determine_root_cause" in result["completed_goals"]

    assert result["tools_used"] == [
        "get_incident_context",
        "check_service_health",
        "extract_errors",
        "retrieve_knowledge",
        "analyze_evidence",
    ]

    assert result["iteration"] == 5

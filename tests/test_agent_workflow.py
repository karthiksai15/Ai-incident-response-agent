from app.graph import agent_workflow


def test_agent_workflow(monkeypatch):

    expected_state = {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [
            "Connection pool exhausted",
        ],
        "retrieved_knowledge": [
            "Database connection pool exhaustion causes connection timeouts."
        ],
        "root_cause": "Database connection pool exhaustion",
        "confidence": 0.95,
        "recommendation": "Investigate database connections.",
        "investigation_notes": [
            "Investigation completed."
        ],
        "current_goal": "determine_root_cause",
        "completed_goals": [
            "understand_context",
            "check_service_health",
            "collect_error_evidence",
            "retrieve_knowledge",
            "determine_root_cause",
        ],
        "next_action": "analyze_evidence",
        "tools_used": [
            "get_incident_context",
            "check_service_health",
            "extract_errors",
            "retrieve_knowledge",
            "analyze_evidence",
        ],
        "iteration": 5,
        "investigation_complete": True,
    }

    def fake_run_agent_investigation(
        state,
        max_iterations,
    ):
        return expected_state

    monkeypatch.setattr(
        agent_workflow,
        "run_agent_investigation",
        fake_run_agent_investigation,
    )

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
        "current_goal": "",
        "completed_goals": [],
        "next_action": "",
        "tools_used": [],
        "iteration": 0,
        "investigation_complete": False,
    }

    result = agent_workflow.agent_workflow.invoke(
        initial_state
    )

    assert result["investigation_complete"] is True
    assert result["root_cause"] == (
        "Database connection pool exhaustion"
    )
    assert result["confidence"] == 0.95
    assert result["recommendation"] == (
        "Investigate database connections."
    )

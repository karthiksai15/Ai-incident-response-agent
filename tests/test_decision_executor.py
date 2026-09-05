from app.agents.decision_executor import execute_decision


def build_state(
    next_action: str,
):
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
        "next_action": next_action,
        "tools_used": [],
        "iteration": 1,
        "investigation_complete": False,
    }


def test_context_action_executes():
    state = build_state(
        "get_incident_context"
    )

    result = execute_decision(state)

    assert isinstance(result, dict)
    assert result["incident_id"] == "INC-001"
    assert result["service"] == "payment-service"
    assert result["severity"] == "HIGH"


def test_health_action_executes():
    state = build_state(
        "check_service_health"
    )

    result = execute_decision(state)

    assert isinstance(result, dict)
    assert result["service"] == "payment-service"
    assert result["status"] == "UNHEALTHY"


def test_error_action_executes():
    state = build_state(
        "extract_errors"
    )

    result = execute_decision(state)

    assert isinstance(result, list)
    assert len(result) > 0

    assert all(
        isinstance(log, dict)
        for log in result
    )

    assert any(
        log["level"] == "ERROR"
        for log in result
    )


def test_search_action_executes():
    state = build_state(
        "search_logs"
    )

    result = execute_decision(state)

    assert isinstance(result, list)
    assert len(result) > 0

    assert all(
        isinstance(log, dict)
        for log in result
    )


def test_rag_action_executes():
    state = build_state(
        "retrieve_knowledge"
    )

    state["evidence"] = [
        "Database connection timeout",
        "Connection pool exhausted",
    ]

    result = execute_decision(state)

    assert result["success"] is True
    assert "knowledge" in result
    assert isinstance(result["knowledge"], list)


def test_analysis_action_executes(monkeypatch):
    state = build_state(
        "analyze_evidence"
    )

    class FakeAnalysis:
        root_cause = "Database connection pool exhaustion"
        confidence = 0.95
        recommendation = "Check database connections."
        evidence = [
            "Connection pool exhausted",
        ]

    monkeypatch.setattr(
        "app.agents.decision_executor.analyze_memory_rag_investigation",
        lambda **kwargs: FakeAnalysis(),
    )

    result = execute_decision(state)

    assert result["root_cause"] == "Database connection pool exhaustion"
    assert result["confidence"] == 0.95
    assert result["recommendation"] == "Check database connections."
    assert result["evidence"] == [
        "Connection pool exhausted",
    ]


def test_unknown_action_is_rejected():
    state = build_state(
        "run_arbitrary_command"
    )

    try:
        execute_decision(state)
        assert False
    except ValueError:
        assert True

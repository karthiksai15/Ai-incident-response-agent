from app.agents.state_updater import (
    update_investigation_state,
)


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


def test_context_updates_state():
    state = build_state(
        "get_incident_context"
    )

    result = {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "status": "OPEN",
        "log_count": 8,
    }

    updated = update_investigation_state(
        state,
        result,
    )

    assert "understand_context" in updated[
        "completed_goals"
    ]

    assert "get_incident_context" in updated[
        "tools_used"
    ]

    assert updated["iteration"] == 2


def test_health_updates_state():
    state = build_state(
        "check_service_health"
    )

    result = {
        "service": "payment-service",
        "status": "UNHEALTHY",
        "response_time_ms": 1250,
        "message": "Database connection issues",
    }

    updated = update_investigation_state(
        state,
        result,
    )

    assert "check_service_health" in updated[
        "completed_goals"
    ]

    assert "check_service_health" in updated[
        "tools_used"
    ]


def test_error_evidence_updates_state():
    state = build_state(
        "extract_errors"
    )

    result = [
        {
            "level": "WARN",
            "message": "Database response time exceeded threshold",
        },
        {
            "level": "ERROR",
            "message": "Connection pool exhausted",
        },
    ]

    updated = update_investigation_state(
        state,
        result,
    )

    assert "collect_error_evidence" in updated[
        "completed_goals"
    ]

    assert "extract_errors" in updated[
        "tools_used"
    ]

    assert len(updated["evidence"]) == 2

    assert (
        "Connection pool exhausted"
        in updated["evidence"]
    )


def test_search_logs_updates_state():
    state = build_state(
        "search_logs"
    )

    result = [
        {
            "level": "ERROR",
            "message": "Database timeout",
        },
        {
            "level": "ERROR",
            "message": "Payment failed",
        },
    ]

    updated = update_investigation_state(
        state,
        result,
    )

    assert "search_log_evidence" in updated[
        "completed_goals"
    ]

    assert "search_logs" in updated[
        "tools_used"
    ]

    assert len(updated["logs"]) == 2


def test_duplicate_tool_is_not_recorded_twice():
    state = build_state(
        "check_service_health"
    )

    state["tools_used"] = [
        "check_service_health"
    ]

    result = {
        "service": "payment-service",
        "status": "UNHEALTHY",
    }

    updated = update_investigation_state(
        state,
        result,
    )

    assert updated["tools_used"].count(
        "check_service_health"
    ) == 1

from app.agents.stopping_conditions import (
    should_stop_investigation,
)


def build_state():
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
        "next_action": "",
        "tools_used": [],
        "iteration": 1,
        "investigation_complete": False,
    }


def test_investigation_continues_initially():
    state = build_state()

    assert (
        should_stop_investigation(state)
        is False
    )


def test_investigation_stops_after_recommendation():
    state = build_state()

    state["completed_goals"] = [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
        "retrieve_knowledge",
        "determine_root_cause",
        "produce_recommendation",
    ]

    assert (
        should_stop_investigation(state)
        is True
    )


def test_investigation_stops_when_root_cause_and_recommendation_exist():
    state = build_state()

    state["root_cause"] = (
        "Database connection pool exhaustion"
    )

    state["recommendation"] = (
        "Investigate database connections."
    )

    assert (
        should_stop_investigation(state)
        is True
    )


def test_root_cause_alone_is_not_enough():
    state = build_state()

    state["root_cause"] = (
        "Database connection pool exhaustion"
    )

    assert (
        should_stop_investigation(state)
        is False
    )


def test_recommendation_alone_is_not_enough():
    state = build_state()

    state["recommendation"] = (
        "Investigate database connections."
    )

    assert (
        should_stop_investigation(state)
        is False
    )

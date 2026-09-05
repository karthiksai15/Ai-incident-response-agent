from app.agents.decision_executor import execute_decision
from app.agents.decision_strategy import decide_next_action
from app.agents.state_updater import update_investigation_state


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
        "current_goal": "understand_context",
        "completed_goals": [],
        "next_action": "get_incident_context",
        "tools_used": [],
        "iteration": 1,
        "investigation_complete": False,
    }


def test_decision_loop_progresses():
    state = build_state()

    # Cycle 1
    result = execute_decision(state)
    state = update_investigation_state(
        state,
        result,
    )

    assert "understand_context" in state[
        "completed_goals"
    ]

    # Decide next action
    state["next_action"] = decide_next_action(
        state["completed_goals"]
    )

    assert state["next_action"] == (
        "check_service_health"
    )

    # Cycle 2
    result = execute_decision(state)
    state = update_investigation_state(
        state,
        result,
    )

    assert "check_service_health" in state[
        "completed_goals"
    ]

    # Decide next action
    state["next_action"] = decide_next_action(
        state["completed_goals"]
    )

    assert state["next_action"] == (
        "extract_errors"
    )

    # Cycle 3
    result = execute_decision(state)
    state = update_investigation_state(
        state,
        result,
    )

    assert "collect_error_evidence" in state[
        "completed_goals"
    ]

    assert len(state["evidence"]) > 0

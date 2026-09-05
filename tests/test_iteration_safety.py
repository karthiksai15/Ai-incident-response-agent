from app.agents.iteration_safety import (
    has_reached_max_iterations,
)


def build_state(iteration: int):
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
        "iteration": iteration,
        "investigation_complete": False,
    }


def test_iteration_below_limit():
    state = build_state(3)

    assert (
        has_reached_max_iterations(
            state,
            max_iterations=5,
        )
        is False
    )


def test_iteration_at_limit():
    state = build_state(5)

    assert (
        has_reached_max_iterations(
            state,
            max_iterations=5,
        )
        is True
    )


def test_iteration_above_limit():
    state = build_state(6)

    assert (
        has_reached_max_iterations(
            state,
            max_iterations=5,
        )
        is True
    )


def test_invalid_max_iterations():
    state = build_state(1)

    try:
        has_reached_max_iterations(
            state,
            max_iterations=0,
        )
        assert False
    except ValueError:
        assert True


def test_default_max_iterations():
    state = build_state(5)

    assert (
        has_reached_max_iterations(state)
        is True
    )

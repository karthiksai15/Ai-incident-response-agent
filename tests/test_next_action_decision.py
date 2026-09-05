from app.agents.decision_strategy import (
    decide_next_action,
    decide_next_goal,
)


def test_initial_goal():
    goal = decide_next_goal([])

    assert goal == "understand_context"


def test_initial_action():
    action = decide_next_action([])

    assert action == "get_incident_context"


def test_health_is_next_after_context():
    completed_goals = [
        "understand_context"
    ]

    goal = decide_next_goal(
        completed_goals
    )

    action = decide_next_action(
        completed_goals
    )

    assert goal == "check_service_health"
    assert action == "check_service_health"


def test_errors_are_next_after_health():
    completed_goals = [
        "understand_context",
        "check_service_health",
    ]

    goal = decide_next_goal(
        completed_goals
    )

    action = decide_next_action(
        completed_goals
    )

    assert goal == "collect_error_evidence"
    assert action == "extract_errors"


def test_rag_is_next_after_errors():
    completed_goals = [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
    ]

    goal = decide_next_goal(
        completed_goals
    )

    action = decide_next_action(
        completed_goals
    )

    assert goal == "retrieve_knowledge"
    assert action == "retrieve_knowledge"


def test_root_cause_is_next_after_rag():
    completed_goals = [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
        "retrieve_knowledge",
    ]

    goal = decide_next_goal(
        completed_goals
    )

    action = decide_next_action(
        completed_goals
    )

    assert goal == "determine_root_cause"
    assert action == "analyze_evidence"


def test_recommendation_is_last():
    completed_goals = [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
        "retrieve_knowledge",
        "determine_root_cause",
    ]

    goal = decide_next_goal(
        completed_goals
    )

    assert goal == ""


def test_completed_investigation_stays_at_final_goal():
    completed_goals = [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
        "retrieve_knowledge",
        "determine_root_cause",
        "produce_recommendation",
    ]

    goal = decide_next_goal(
        completed_goals
    )

    assert goal == ""

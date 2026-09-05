import pytest

from app.agents.decision_strategy import choose_next_action


def test_context_goal_selects_context_tool():
    action = choose_next_action(
        "understand_context"
    )

    assert action == "get_incident_context"


def test_health_goal_selects_health_tool():
    action = choose_next_action(
        "check_service_health"
    )

    assert action == "check_service_health"


def test_error_goal_selects_error_tool():
    action = choose_next_action(
        "collect_error_evidence"
    )

    assert action == "extract_errors"


def test_search_goal_selects_search_tool():
    action = choose_next_action(
        "search_log_evidence"
    )

    assert action == "search_logs"


def test_root_cause_goal_selects_analysis():
    action = choose_next_action(
        "determine_root_cause"
    )

    assert action == "analyze_evidence"


def test_unknown_goal_is_rejected():
    with pytest.raises(ValueError):
        choose_next_action(
            "unknown_goal"
        )


def test_empty_goal_is_rejected():
    with pytest.raises(ValueError):
        choose_next_action("")


def test_non_string_goal_is_rejected():
    with pytest.raises(ValueError):
        choose_next_action(None)

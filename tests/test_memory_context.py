import pytest

from app.agents.decision_strategy import build_memory_context


def test_memory_context_when_incidents_exist():

    result = build_memory_context(
        [
            "Previous database pool exhaustion incident."
        ]
    )

    assert result == (
        "Relevant historical incidents are available "
        "as supporting evidence."
    )


def test_memory_context_when_no_incidents_exist():

    result = build_memory_context([])

    assert result == (
        "No relevant historical incidents are available."
    )


def test_memory_context_rejects_invalid_input():

    with pytest.raises(ValueError):
        build_memory_context("invalid")

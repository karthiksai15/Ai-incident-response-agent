import pytest

from app.agents.decision_strategy import has_relevant_memory


def test_has_relevant_memory():

    assert has_relevant_memory(
        [
            "Previous database connection pool incident."
        ]
    ) is True


def test_has_no_relevant_memory():

    assert has_relevant_memory([]) is False


def test_rejects_invalid_memory():

    with pytest.raises(ValueError):
        has_relevant_memory("invalid")

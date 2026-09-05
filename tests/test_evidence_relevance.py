import pytest

from evaluation.metrics.evidence_relevance import (
    calculate_evidence_recall,
)


def test_evidence_recall():

    predicted = [
        "Connection pool exhausted",
        "Payment request failed",
    ]

    expected = [
        "Connection pool exhausted",
        "Failed to acquire JDBC connection",
    ]

    result = calculate_evidence_recall(
        predicted=predicted,
        expected=expected,
    )

    assert result == 0.5


def test_evidence_recall_is_case_insensitive():

    result = calculate_evidence_recall(
        predicted=["CONNECTION POOL EXHAUSTED"],
        expected=["Connection pool exhausted"],
    )

    assert result == 1.0


def test_evidence_recall_rejects_empty_expected():

    with pytest.raises(ValueError):
        calculate_evidence_recall(
            predicted=["Some evidence"],
            expected=[],
        )

import pytest

from evaluation.metrics.root_cause_accuracy import (
    calculate_root_cause_accuracy,
)


def test_root_cause_accuracy():

    predicted = [
        "Database connection pool exhaustion",
        "Redis failure",
        "Wrong root cause",
        "Service crash",
    ]

    expected = [
        "Database connection pool exhaustion",
        "Redis failure",
        "High API latency",
        "Service crash",
    ]

    result = calculate_root_cause_accuracy(
        predicted=predicted,
        expected=expected,
    )

    assert result == 0.75


def test_root_cause_accuracy_ignores_case_and_whitespace():

    result = calculate_root_cause_accuracy(
        predicted=[
            "  DATABASE CONNECTION POOL EXHAUSTION "
        ],
        expected=[
            "Database connection pool exhaustion"
        ],
    )

    assert result == 1.0


def test_root_cause_accuracy_rejects_mismatched_lengths():

    with pytest.raises(ValueError):
        calculate_root_cause_accuracy(
            predicted=["Database failure"],
            expected=[
                "Database failure",
                "Redis failure",
            ],
        )

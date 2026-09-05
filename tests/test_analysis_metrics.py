import pytest

from evaluation.metrics.analysis_metrics import accuracy


def test_accuracy():
    predictions = [
        "database connection pool exhaustion",
        "redis failure",
        "service crash",
    ]

    expected = [
        "database connection pool exhaustion",
        "redis failure",
        "high api latency",
    ]

    result = accuracy(
        predictions=predictions,
        expected=expected,
    )

    assert result == pytest.approx(2 / 3)


def test_perfect_accuracy():
    predictions = [
        "database connection pool exhaustion",
        "redis failure",
    ]

    expected = [
        "database connection pool exhaustion",
        "redis failure",
    ]

    result = accuracy(
        predictions=predictions,
        expected=expected,
    )

    assert result == 1.0


def test_mismatched_lengths():
    with pytest.raises(ValueError):
        accuracy(
            predictions=["redis failure"],
            expected=[
                "redis failure",
                "service crash",
            ],
        )


def test_empty_expected():
    with pytest.raises(ValueError):
        accuracy(
            predictions=[],
            expected=[],
        )

import pytest

from evaluation.metrics.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
)


def test_recall_at_k_found():
    retrieved = [
        "high_api_latency.md",
        "database_connection_pool.md",
        "redis_failure.md",
    ]

    expected = [
        "database_connection_pool.md"
    ]

    assert recall_at_k(
        retrieved,
        expected,
        2,
    ) == 1.0


def test_recall_at_k_not_found():
    retrieved = [
        "redis_failure.md",
        "service_crash.md",
    ]

    expected = [
        "database_connection_pool.md"
    ]

    assert recall_at_k(
        retrieved,
        expected,
        2,
    ) == 0.0


def test_precision_at_k():
    retrieved = [
        "database_connection_pool.md",
        "redis_failure.md",
        "service_crash.md",
    ]

    expected = [
        "database_connection_pool.md"
    ]

    assert precision_at_k(
        retrieved,
        expected,
        3,
    ) == pytest.approx(1 / 3)


def test_precision_at_k_all_relevant():
    retrieved = [
        "database_connection_pool.md",
    ]

    expected = [
        "database_connection_pool.md"
    ]

    assert precision_at_k(
        retrieved,
        expected,
        1,
    ) == 1.0


def test_invalid_recall_k():
    with pytest.raises(ValueError):
        recall_at_k(
            ["test.md"],
            ["test.md"],
            0,
        )


def test_empty_expected_sources():
    with pytest.raises(ValueError):
        recall_at_k(
            ["test.md"],
            [],
            3,
        )

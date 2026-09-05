import pytest

from evaluation.metrics.memory_relevance import (
    calculate_memory_precision,
)


def test_memory_precision():

    retrieved = [
        "MEM-001",
        "MEM-003",
        "MEM-009",
    ]

    relevant = [
        "MEM-001",
        "MEM-003",
    ]

    result = calculate_memory_precision(
        retrieved_ids=retrieved,
        relevant_ids=relevant,
    )

    assert result == pytest.approx(2 / 3)


def test_memory_precision_all_relevant():

    result = calculate_memory_precision(
        retrieved_ids=[
            "MEM-001",
            "MEM-002",
        ],
        relevant_ids=[
            "MEM-001",
            "MEM-002",
        ],
    )

    assert result == 1.0


def test_memory_precision_rejects_empty_retrieval():

    with pytest.raises(ValueError):
        calculate_memory_precision(
            retrieved_ids=[],
            relevant_ids=["MEM-001"],
        )

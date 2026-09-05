import pytest

from evaluation.metrics.investigation_success import (
    calculate_investigation_success,
)


def test_success_when_investigation_is_correct():

    result = calculate_investigation_success(
        root_cause_accuracy=1.0,
        evidence_recall=1.0,
    )

    assert result == 1.0


def test_failure_when_evidence_is_incomplete():

    result = calculate_investigation_success(
        root_cause_accuracy=1.0,
        evidence_recall=0.5,
    )

    assert result == 0.0


def test_rejects_invalid_metric():

    with pytest.raises(ValueError):
        calculate_investigation_success(
            root_cause_accuracy=1.2,
            evidence_recall=1.0,
        )

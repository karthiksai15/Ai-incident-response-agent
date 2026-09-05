from unittest.mock import patch

from evaluation.runners.configurations import (
    ExperimentConfiguration,
)
from evaluation.runners.experiment import (
    run_single_experiment,
)


class FakeAnalysis:
    root_cause = "Database connection pool exhaustion"
    evidence = [
        "Connection pool exhausted"
    ]
    confidence = 0.9
    recommendation = "Check active database connections."


def test_run_single_experiment():

    incident = {
        "incident_id": "EVAL-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [
            "Connection pool exhausted"
        ],
        "expected_root_cause": (
            "Database connection pool exhaustion"
        ),
        "expected_evidence": [
            "Connection pool exhausted"
        ],
    }

    with patch(
        "evaluation.runners.experiment.run_analysis",
        return_value=FakeAnalysis(),
    ) as mock_analysis:

        result = run_single_experiment(
            incident=incident,
            configuration=(
                ExperimentConfiguration.RAG_MEMORY
            ),
            runbooks=[
                "Database connection pool troubleshooting"
            ],
            similar_incidents=[
                "MEM-001: Database pool exhaustion"
            ],
        )

    assert result["incident_id"] == "EVAL-001"
    assert result["configuration"] == "llm_rag_memory"
    assert (
        result["root_cause"]
        == "Database connection pool exhaustion"
    )
    assert result["confidence"] == 0.9

    mock_analysis.assert_called_once()

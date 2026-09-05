from unittest.mock import patch

from evaluation.runners.analysis_adapter import (
    run_analysis,
)
from evaluation.runners.configurations import (
    ExperimentConfiguration,
)


def test_llm_only_configuration():

    with patch(
        "evaluation.runners.analysis_adapter.analyze_with_llm"
    ) as mock_analysis:

        run_analysis(
            configuration=ExperimentConfiguration.LLM_ONLY,
            incident_id="EVAL-001",
            service="payment-service",
            severity="HIGH",
            evidence=[
                "Connection pool exhausted"
            ],
        )

        mock_analysis.assert_called_once()


def test_rag_configuration():

    with patch(
        "evaluation.runners.analysis_adapter.analyze_investigation"
    ) as mock_analysis:

        run_analysis(
            configuration=ExperimentConfiguration.RAG,
            incident_id="EVAL-001",
            service="payment-service",
            severity="HIGH",
            evidence=[
                "Connection pool exhausted"
            ],
            runbooks=[
                "Database connection pool troubleshooting"
            ],
        )

        mock_analysis.assert_called_once()


def test_memory_configuration():

    with patch(
        "evaluation.runners.analysis_adapter.analyze_memory_rag_investigation"
    ) as mock_analysis:

        run_analysis(
            configuration=ExperimentConfiguration.RAG_MEMORY,
            incident_id="EVAL-001",
            service="payment-service",
            severity="HIGH",
            evidence=[
                "Connection pool exhausted"
            ],
            runbooks=[
                "Database connection pool troubleshooting"
            ],
            similar_incidents=[
                "MEM-001: Database pool exhaustion"
            ],
        )

        mock_analysis.assert_called_once()

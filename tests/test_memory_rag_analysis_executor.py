from unittest.mock import patch

from app.agents.analysis_executor import (
    analyze_memory_rag_investigation,
)


def test_memory_rag_analysis_executor():
    with patch(
        "app.agents.analysis_executor.analyze_with_llm"
    ) as mock_llm:

        mock_llm.return_value = {
            "root_cause": "Database connection pool exhaustion",
            "confidence": 0.9,
            "evidence": [
                "Connection pool exhausted",
            ],
            "recommendation": "Investigate database connections.",
        }

        result = analyze_memory_rag_investigation(
            incident_id="INC-001",
            service="payment-service",
            severity="HIGH",
            evidence=[
                "Connection pool exhausted",
            ],
            runbooks=[
                "Check database connection pool configuration.",
            ],
            similar_incidents=[
                "Previous incident involved connection exhaustion.",
            ],
        )

        assert result["root_cause"] == (
            "Database connection pool exhaustion"
        )

        prompt = mock_llm.call_args.kwargs["prompt"]

        assert "CURRENT INCIDENT EVIDENCE" in prompt
        assert "OFFICIAL RUNBOOK KNOWLEDGE" in prompt
        assert "SIMILAR HISTORICAL INCIDENTS" in prompt

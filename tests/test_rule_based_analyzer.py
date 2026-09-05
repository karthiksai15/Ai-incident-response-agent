from evaluation.baselines.rule_based_analyzer import (
    analyze_incident,
)


def test_database_incident():
    result = analyze_incident(
        "INC-001"
    )

    assert result.incident_id == "INC-001"

    assert (
        result.root_cause
        == "database connection pool exhaustion"
    )

    assert result.confidence > 0

    assert len(result.evidence) > 0

    assert any(
        "connection pool exhausted" in evidence.lower()
        for evidence in result.evidence
    )

    assert (
        "connection pool"
        in result.recommendation.lower()
    )

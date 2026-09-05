import pytest
from pydantic import ValidationError

from app.models.analysis import IncidentAnalysis


def test_valid_analysis():

    analysis = IncidentAnalysis(
        incident_id="INC-001",
        root_cause="database connection pool exhaustion",
        confidence=0.95,
        evidence=[
            "Connection pool exhausted",
            "Failed to acquire JDBC connection",
        ],
        recommendation=(
            "Investigate database connection pool utilization."
        ),
    )

    assert analysis.incident_id == "INC-001"
    assert analysis.confidence == 0.95
    assert len(analysis.evidence) == 2


def test_confidence_cannot_exceed_one():

    with pytest.raises(ValidationError):

        IncidentAnalysis(
            incident_id="INC-001",
            root_cause="database connection pool exhaustion",
            confidence=1.5,
            evidence=[],
            recommendation="Investigate the database.",
        )


def test_confidence_cannot_be_negative():

    with pytest.raises(ValidationError):

        IncidentAnalysis(
            incident_id="INC-001",
            root_cause="database connection pool exhaustion",
            confidence=-0.1,
            evidence=[],
            recommendation="Investigate the database.",
        )

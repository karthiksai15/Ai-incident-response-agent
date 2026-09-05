import pytest

from app.services.incident_ingestion import ingest_incident


def test_ingest_incident():

    incident = ingest_incident(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
    )

    assert incident.incident_id == "INC-001"
    assert incident.service == "payment-service"
    assert incident.severity == "HIGH"
    assert incident.status == "OPEN"

    assert len(incident.logs) == 8

    assert incident.logs[2].level == "WARN"
    assert incident.logs[4].message == "Connection pool exhausted"


def test_missing_incident_log():

    with pytest.raises(FileNotFoundError):
        ingest_incident(
            incident_id="INC-999",
            service="payment-service",
            severity="HIGH",
        )

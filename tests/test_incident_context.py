import pytest

from app.tools.incident_context import get_incident_context


def test_get_incident_context():
    context = get_incident_context(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
    )

    assert context.incident_id == "INC-001"
    assert context.service == "payment-service"
    assert context.severity == "HIGH"
    assert context.status == "OPEN"
    assert context.log_count == 8


def test_context_is_structured():
    context = get_incident_context(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
    )

    assert hasattr(context, "incident_id")
    assert hasattr(context, "service")
    assert hasattr(context, "severity")
    assert hasattr(context, "status")
    assert hasattr(context, "log_count")


def test_missing_incident():
    with pytest.raises(FileNotFoundError):
        get_incident_context(
            incident_id="INC-999",
            service="payment-service",
            severity="HIGH",
        )

from app.tools.error_extraction import extract_errors
from app.tools.incident_context import get_incident_context
from app.tools.log_search import search_logs
from app.tools.service_health import check_service_health


def test_incident_investigation_flow():
    incident_id = "INC-001"
    service = "payment-service"
    severity = "HIGH"

    logs = search_logs(incident_id)

    assert len(logs) == 8

    errors = extract_errors(incident_id)

    assert len(errors) == 6
    assert any(
        "Connection pool exhausted" in log.message
        for log in errors
    )

    health = check_service_health(service)

    assert health.status == "UNHEALTHY"
    assert health.response_time_ms == 1250

    context = get_incident_context(
        incident_id=incident_id,
        service=service,
        severity=severity,
    )

    assert context.incident_id == incident_id
    assert context.service == service
    assert context.severity == severity
    assert context.status == "OPEN"
    assert context.log_count == 8


def test_investigation_evidence_is_consistent():
    incident_id = "INC-001"

    logs = search_logs(incident_id)
    errors = extract_errors(incident_id)

    assert len(errors) <= len(logs)

    error_messages = [
        log.message
        for log in errors
    ]

    assert "Connection pool exhausted" in error_messages
    assert "Failed to acquire JDBC connection" in error_messages
    assert "Payment request failed: PAY-101" in error_messages

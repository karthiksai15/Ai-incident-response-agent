from app.tools.service_health import check_service_health


def test_payment_service_unhealthy():
    health = check_service_health("payment-service")

    assert health.service == "payment-service"
    assert health.status == "UNHEALTHY"
    assert health.response_time_ms == 1250
    assert "database" in health.message.lower()


def test_auth_service_healthy():
    health = check_service_health("auth-service")

    assert health.service == "auth-service"
    assert health.status == "HEALTHY"
    assert health.response_time_ms == 120


def test_unknown_service():
    health = check_service_health("unknown-service")

    assert health.service == "unknown-service"
    assert health.status == "UNKNOWN"
    assert health.response_time_ms == 0


def test_health_result_is_structured():
    health = check_service_health("payment-service")

    assert hasattr(health, "service")
    assert hasattr(health, "status")
    assert hasattr(health, "response_time_ms")
    assert hasattr(health, "message")

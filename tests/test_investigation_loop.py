from app.agents.tool_calling import execute_tool_call


class MockFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


def test_execute_get_incident_context():
    function_call = MockFunctionCall(
        name="get_incident_context",
        args={
            "incident_id": "INC-001",
            "service": "payment-service",
            "severity": "HIGH",
        },
    )

    result = execute_tool_call(function_call)

    assert result["incident_id"] == "INC-001"
    assert result["service"] == "payment-service"
    assert result["severity"] == "HIGH"
    assert result["status"] == "OPEN"


def test_execute_check_service_health():
    function_call = MockFunctionCall(
        name="check_service_health",
        args={
            "service": "payment-service",
        },
    )

    result = execute_tool_call(function_call)

    assert result["service"] == "payment-service"
    assert result["status"] == "UNHEALTHY"
    assert result["response_time_ms"] == 1250


def test_execute_extract_errors():
    function_call = MockFunctionCall(
        name="extract_errors",
        args={
            "incident_id": "INC-001",
        },
    )

    result = execute_tool_call(function_call)

    assert len(result) > 0

    messages = [
        item["message"]
        for item in result
    ]

    assert any(
        "connection pool exhausted" in message.lower()
        for message in messages
    )

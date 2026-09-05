import pytest

from app.agents.tool_safety import (
    is_tool_allowed,
    validate_tool_call,
)


def test_read_only_tool_is_allowed():
    assert is_tool_allowed("search_logs")
    assert is_tool_allowed("extract_errors")
    assert is_tool_allowed("check_service_health")
    assert is_tool_allowed("get_incident_context")


def test_unknown_tool_is_rejected():
    assert not is_tool_allowed("delete_database")


def test_valid_search_logs_arguments():
    validate_tool_call(
        "search_logs",
        {
            "incident_id": "INC-001",
            "level": "ERROR",
        },
    )


def test_invalid_incident_id_is_rejected():
    with pytest.raises(ValueError):
        validate_tool_call(
            "search_logs",
            {
                "incident_id": "../../etc/passwd",
            },
        )


def test_invalid_tool_is_rejected():
    with pytest.raises(PermissionError):
        validate_tool_call(
            "restart_server",
            {
                "service": "payment-service",
            },
        )


def test_invalid_severity_is_rejected():
    with pytest.raises(ValueError):
        validate_tool_call(
            "get_incident_context",
            {
                "incident_id": "INC-001",
                "service": "payment-service",
                "severity": "DANGEROUS",
            },
        )


class MockFunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


def test_execute_tool_call_rejects_unknown_tool():
    from app.agents.tool_calling import execute_tool_call

    function_call = MockFunctionCall(
        name="delete_database",
        args={},
    )

    with pytest.raises(PermissionError):
        execute_tool_call(function_call)


def test_execute_tool_call_rejects_malicious_incident_id():
    from app.agents.tool_calling import execute_tool_call

    function_call = MockFunctionCall(
        name="search_logs",
        args={
            "incident_id": "../../etc/passwd",
        },
    )

    with pytest.raises(ValueError):
        execute_tool_call(function_call)

from app.tools.error_handler import handle_tool_error


def test_validation_error():
    result = handle_tool_error(
        ValueError("Invalid incident_id format")
    )

    assert result.success is False
    assert result.error_type == "VALIDATION_ERROR"
    assert result.message == "Invalid incident_id format"


def test_file_not_found_error():
    result = handle_tool_error(
        FileNotFoundError("Log file not found")
    )

    assert result.success is False
    assert result.error_type == "TOOL_ERROR"
    assert result.message == "Log file not found"


def test_unexpected_error():
    result = handle_tool_error(
        RuntimeError("Internal failure")
    )

    assert result.success is False
    assert result.error_type == "TOOL_ERROR"
    assert result.message == "An unexpected tool error occurred."


def test_tool_result_success():
    from app.tools.tool_result import ToolResult

    result = ToolResult(
        success=True,
        data={"status": "healthy"},
    )

    assert result.success is True
    assert result.data["status"] == "healthy"

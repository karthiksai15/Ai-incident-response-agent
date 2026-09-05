from app.tools.tool_result import ToolResult


def handle_tool_error(error: Exception) -> ToolResult:
    """
    Convert Python exceptions into structured tool errors.
    """

    if isinstance(error, ValueError):
        return ToolResult(
            success=False,
            error_type="VALIDATION_ERROR",
            message=str(error),
        )

    if isinstance(error, FileNotFoundError):
        return ToolResult(
            success=False,
            error_type="TOOL_ERROR",
            message=str(error),
        )

    return ToolResult(
        success=False,
        error_type="TOOL_ERROR",
        message="An unexpected tool error occurred.",
    )

from app.tools.validation import (
    validate_incident_id,
    validate_service,
    validate_log_level,
)


READ_ONLY_TOOLS = {
    "search_logs",
    "extract_errors",
    "check_service_health",
    "get_incident_context",
}


def is_tool_allowed(tool_name: str) -> bool:
    return tool_name in READ_ONLY_TOOLS


def validate_tool_call(
    tool_name: str,
    arguments: dict,
) -> None:

    if not isinstance(tool_name, str):
        raise ValueError("tool_name must be a string")

    if not is_tool_allowed(tool_name):
        raise PermissionError(
            f"Tool is not allowed: {tool_name}"
        )

    if not isinstance(arguments, dict):
        raise ValueError(
            "Tool arguments must be a dictionary"
        )

    if tool_name == "search_logs":
        validate_incident_id(
            arguments.get("incident_id")
        )
        validate_log_level(
            arguments.get("level")
        )

    elif tool_name == "extract_errors":
        validate_incident_id(
            arguments.get("incident_id")
        )

    elif tool_name == "check_service_health":
        validate_service(
            arguments.get("service")
        )

    elif tool_name == "get_incident_context":
        validate_incident_id(
            arguments.get("incident_id")
        )
        validate_service(
            arguments.get("service")
        )

        severity = arguments.get("severity")

        if not isinstance(severity, str):
            raise ValueError(
                "severity must be a string"
            )

        if severity.strip().upper() not in {
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        }:
            raise ValueError(
                "Invalid severity"
            )

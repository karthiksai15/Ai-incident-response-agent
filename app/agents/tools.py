from app.tools.log_search import search_logs
from app.tools.error_extraction import extract_errors
from app.tools.service_health import check_service_health
from app.tools.incident_context import get_incident_context


SEARCH_LOGS_TOOL = {
    "name": "search_logs",
    "description": (
        "Search logs for a specific incident. "
        "Use this when you need to find logs matching "
        "a specific severity level or keyword."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "incident_id": {
                "type": "string",
                "description": "Incident ID, for example INC-001.",
            },
            "level": {
                "type": "string",
                "description": "Optional log level: INFO, WARN, or ERROR.",
            },
            "keyword": {
                "type": "string",
                "description": "Optional keyword to search in log messages.",
            },
        },
        "required": ["incident_id"],
    },
}


EXTRACT_ERRORS_TOOL = {
    "name": "extract_errors",
    "description": (
        "Extract WARN and ERROR logs for a specific incident. "
        "Use this when investigating the important failure "
        "evidence in an incident."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "incident_id": {
                "type": "string",
                "description": "Incident ID, for example INC-001.",
            },
        },
        "required": ["incident_id"],
    },
}


CHECK_SERVICE_HEALTH_TOOL = {
    "name": "check_service_health",
    "description": (
        "Check the current simulated health of a service. "
        "Use this when you need to determine whether a "
        "service is healthy or unhealthy."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service": {
                "type": "string",
                "description": "Service name, for example payment-service.",
            },
        },
        "required": ["service"],
    },
}


GET_INCIDENT_CONTEXT_TOOL = {
    "name": "get_incident_context",
    "description": (
        "Get basic context for an incident including "
        "service, severity, status, and log count."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "incident_id": {
                "type": "string",
                "description": "Incident ID, for example INC-001.",
            },
            "service": {
                "type": "string",
                "description": "Service associated with the incident.",
            },
            "severity": {
                "type": "string",
                "description": "Incident severity.",
            },
        },
        "required": [
            "incident_id",
            "service",
            "severity",
        ],
    },
}


def execute_search_logs(
    incident_id: str,
    level: str | None = None,
    keyword: str | None = None,
):
    return search_logs(
        incident_id=incident_id,
        level=level,
        keyword=keyword,
    )


def execute_extract_errors(
    incident_id: str,
):
    return extract_errors(
        incident_id=incident_id,
    )


def execute_check_service_health(
    service: str,
):
    return check_service_health(
        service=service,
    )


def execute_get_incident_context(
    incident_id: str,
    service: str,
    severity: str,
):
    return get_incident_context(
        incident_id=incident_id,
        service=service,
        severity=severity,
    )

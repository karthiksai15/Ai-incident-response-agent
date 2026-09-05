from app.models.incident import LogEntry
from app.tools.log_search import search_logs


def extract_errors(
    incident_id: str,
) -> list[LogEntry]:
    """
    Extract WARN and ERROR logs for an incident.

    Args:
        incident_id: Incident identifier.

    Returns:
        WARN and ERROR log entries.
    """

    logs = search_logs(incident_id)

    return [
        log
        for log in logs
        if log.level.upper() in {"WARN", "ERROR"}
    ]
